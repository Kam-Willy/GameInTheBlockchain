# main.py
from game.snake import SnakeGame
from game.user import Player

import os

if __name__ == "__main__":
    os.makedirs("screenshots", exist_ok=True)
    name = input("Enter your name: ")
    address = input("Enter your Ethereum wallet address: ")
    player = Player(name=name, wallet_address=address)

    print(f"Welcome, {player.name}! Your ID is {player.id} ! Your address is {player.address}")

    game = SnakeGame(player)
    game.game_loop()
