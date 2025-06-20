import random
import os
import time
import threading
from PyQt5.QtWidgets import QApplication
import pygame
from datetime import datetime
from game.scoreboard_ui import view_scoreboard
from game.scoreboard import Scoreboard
from blockchain.score_chain import record_score_on_chain
from blockchain.nft_service import upload_to_ipfs, upload_metadata, mint_nft


WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED   = (255, 0, 0)
BLACK = (0, 0, 0)

FOOD_TYPES = {
    "regular": {"points": 1, "emoji": "🍎"},
    "spider": {"points": 2, "emoji": "🕷️"},
    "rat": {"points": 4, "emoji": "🐀"},
    "rabbit": {"points": 8, "emoji": "🐰"},
    "pig": {"points": 16, "emoji": "🐷"},
}


class SnakeGame:
    def __init__(self, player, width=600, height=400, block_size=20):
        pygame.init()
        self.width = width
        self.height = height
        self.block_size = block_size
        self.food_eaten = 0  # Count of regular food eaten
        self.super_foods = []  # Active superfoods on screen
        self.superfoods_spawned = 0
        self.superfood_timer = None
        self.emoji_font = pygame.font.SysFont("Segoe UI Emoji", self.block_size)
        self.player = player
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(f"Snake Game - {player.name}")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 25)
        self.scoreboard = Scoreboard()

        self.reset()

    def reset(self):
        self.snake = [[100, 50]]
        self.direction = 'RIGHT'
        self.food = self.generate_food()
        self.score = 0
        self.superfoods = []
        self.superfoods_spawned = 0
        self.superfood_timer = None

    def generate_food(self, food_type="regular"):
	    x = random.randint(0, (self.width - self.block_size) // self.block_size) * self.block_size
	    y = random.randint(0, (self.height - self.block_size) // self.block_size) * self.block_size

	    return {"pos": [x, y], "type": food_type}

    def draw_snake(self):
        for block in self.snake:
            pygame.draw.rect(self.window, GREEN, pygame.Rect(block[0], block[1], self.block_size, self.block_size))

    def display_score(self):
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.window.blit(score_text, [10, 10])

    def save_game_state(self):
        filename = f"{self.player.name}_{self.player.id[:6]}_{self.score}_{len(self.snake)}.png"
        filepath = os.path.join("screenshots", filename)
        pygame.image.save(self.window, filepath)

        return filepath

    def maybe_spawn_superfood(self):
	    # One superfood per every 10 points
	    if self.score // 10 > self.superfoods_spawned and not self.superfoods:
	        kind = random.choice([k for k in FOOD_TYPES if k != "regular"])
	        food_x = random.randint(0, (self.width - self.block_size) // self.block_size) * self.block_size
	        food_y = random.randint(0, (self.height - self.block_size) // self.block_size) * self.block_size
	        self.superfoods.append({"type": kind, "pos": [food_x, food_y], "spawn_time": time.time()})
	        self.superfoods_spawned += 1  # Track how many superfoods have appeared

    def handle_blockchain_tasks(self, screenshot):
        print("🧵 Background thread running...")  # Debug: confirms thread starts
        try:
            print(f"📸 Saved game snapshot at: {screenshot}")
            img_url = upload_to_ipfs(screenshot)
            metadata_url = upload_metadata(img_url, self.player.name, self.score, len(self.snake))
            tx_hash = mint_nft(metadata_url)
            print("✅ NFT Minted! Tx:", tx_hash)

            record_score_on_chain(
                player_name=self.player.name,
                player_address=self.player.address,
                score=self.score
            )
        except Exception as e:
            print("⚠️ Blockchain or IPFS error:", e)

    def game_over_screen(self):
        # Step 1: Update local scoreboard (on-chain write is in background)
        self.scoreboard.update_score(
            player_id=self.player.id,
            player_name=self.player.name,
            player_address=self.player.address,
            score=self.score
        )

        # Step 2: Show Game Over UI immediately
        self.window.fill(BLACK)
        message = self.font.render("Game Over! R=Restart   Q=Quit   V=View Scores", True, RED)
        self.window.blit(message, [self.width // 8, self.height // 2])
        pygame.display.update()

        pygame.time.wait(500)
        screenshot = self.save_game_state()

        # Step 3: Launch blockchain operations in the background
        thread = threading.Thread(target=self.handle_blockchain_tasks, args=(screenshot,), daemon=True)
        thread.start()

        print("⏳ Blockchain thread started...")

        # Step 4: Wait for input to show UI
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        exit()
                    elif event.key == pygame.K_r:
                        self.reset_game()
                        self.game_loop()
                        return
                    elif event.key == pygame.K_v:
                        # 🔁 Display raw local game data for the session
                        player_data = [{
                            "name": self.player.name,
                            "player": self.player.address,
                            "score": self.score
                        }]
                        total_data = [{
                            "name": self.player.name,
                            "player": self.player.address,
                            "total_score": self.score
                        }]
                        highest_data = [{
                            "name": self.player.name,
                            "player": self.player.address,
                            "highest_score": self.score
                        }]
                        view_scoreboard(highest_data, total_data, player_data)

            # Allow redraw in case it's covered
            self.window.fill(BLACK)
            self.window.blit(message, [self.width // 8, self.height // 2])
            pygame.display.update()
            self.clock.tick(10)

    def reset_game(self):
	    self.snake = [[self.width // 2, self.height // 2]]
	    self.food = self.generate_food()
	    self.score = 0
	    self.direction = 'RIGHT'

    def game_loop(self):
	    running = True
	    paused = False
	    speed = 5  # Initial snake speed (lower = slower)

	    while running:
	        for event in pygame.event.get():
	            if event.type == pygame.QUIT:
	                running = False
	            elif event.type == pygame.KEYDOWN:
	                if event.key == pygame.K_p:
	                    paused = not paused  # Toggle pause
	                if not paused:
	                    if event.key == pygame.K_UP and self.direction != 'DOWN':
	                        self.direction = 'UP'
	                    elif event.key == pygame.K_DOWN and self.direction != 'UP':
	                        self.direction = 'DOWN'
	                    elif event.key == pygame.K_LEFT and self.direction != 'RIGHT':
	                        self.direction = 'LEFT'
	                    elif event.key == pygame.K_RIGHT and self.direction != 'LEFT':
	                        self.direction = 'RIGHT'

	        if paused:
	            pause_text = self.font.render("Paused - Press 'P' to Resume", True, WHITE)
	            self.window.blit(pause_text, [self.width // 4, self.height // 2])
	            pygame.display.update()
	            self.clock.tick(5)
	            continue

	        # Move snake
	        x, y = self.snake[0]
	        if self.direction == 'UP':
	            y -= self.block_size
	        elif self.direction == 'DOWN':
	            y += self.block_size
	        elif self.direction == 'LEFT':
	            x -= self.block_size
	        elif self.direction == 'RIGHT':
	            x += self.block_size

	        new_head = [x, y]

	        # Game Over Check
	        if (x < 0 or x >= self.width or y < 0 or y >= self.height or new_head in self.snake):
	            print(f"Game Over! Score: {self.score}, Length: {len(self.snake)}")
	            screenshot = self.save_game_state()
	            print(f"Saved game snapshot at: {screenshot}")
	            self.game_over_screen()
	            return

	        self.snake.insert(0, new_head)

	        # Eat regular food
	        if pygame.Rect(new_head[0], new_head[1], self.block_size, self.block_size).colliderect(
	            pygame.Rect(self.food["pos"][0], self.food["pos"][1], self.block_size, self.block_size)
	        ):
	            self.score += 1
	            self.food = self.generate_food()
	            speed = min(20, speed + 0.5)  # Increase speed gradually
	        else:
	            # Check for superfood collision
	            eaten = False
	            for sf in self.superfoods:
	                if pygame.Rect(new_head[0], new_head[1], self.block_size, self.block_size).colliderect(
	                    pygame.Rect(sf["pos"][0], sf["pos"][1], self.block_size, self.block_size)
	                ):
	                    points = FOOD_TYPES[sf["type"]]["points"]
	                    self.score += points
	                    for _ in range(points - 1):
	                        self.snake.insert(0, new_head.copy())
	                    eaten = True
	                    break

	            if eaten:
	                self.superfoods.clear()
	            else:
	                self.snake.pop()

	        # Maybe spawn superfood
	        self.maybe_spawn_superfood()

	        # Remove expired superfood
	        if self.superfoods and (time.time() - self.superfoods[0]["spawn_time"] > 5):
	            self.superfoods.clear()

	        # === DRAWING ===
	        self.window.fill(BLACK)
	        self.draw_snake()

	        # Draw superfoods
	        for sf in self.superfoods:
	            emoji = FOOD_TYPES[sf["type"]]["emoji"]
	            emoji_surface = self.emoji_font.render(emoji, True, WHITE)
	            self.window.blit(emoji_surface, sf["pos"])

	        # Draw regular food
	        emoji = FOOD_TYPES[self.food["type"]]["emoji"]
	        emoji_surface = self.emoji_font.render(emoji, True, WHITE)
	        self.window.blit(emoji_surface, self.food["pos"])

	        self.display_score()
	        pygame.display.update()
	        self.clock.tick(speed)

    pygame.quit()
