# game/scoreboard.py
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from blockchain.score_chain import record_score_on_chain, fetch_all_scores

SCORE_FILE = Path("game/scoreboard_data.json")


class Scoreboard:
    def __init__(self):
        self.scores = {}

    def update_score(self, player_id, player_name, score, player_address):
        try:
            record_score_on_chain(
                player_name=player_name,
                player_address=player_address,
                score=score
            )
        except Exception as e:
            print("⚠️ Could not push score on-chain:", e)

    def get_total_scores(self):
        all_scores = fetch_all_scores()
        leaderboard = {}
        for score in all_scores:
            addr = score["player"]
            if addr not in leaderboard:
                leaderboard[addr] = {
                    "name": score["name"],
                    "total_score": 0
                }
            leaderboard[addr]["total_score"] += score["score"]

        return sorted(
            [{"name": v["name"], "total_score": v["total_score"]} for v in leaderboard.values()],
            key=lambda x: x["total_score"],
            reverse=True
        )

    def get_highest_scores(self):
        all_scores = fetch_all_scores()
        scores = sorted(all_scores, key=lambda x: x["score"], reverse=True)
        return [{"name": s["name"], "highest_score": s["score"]} for s in scores[:10]]

    def get_player_score(self, player_id_or_address):
        all_scores = fetch_all_scores()
        filtered = [s for s in all_scores if s["player"].lower() == player_id_or_address.lower()]
        if not filtered:
            return []
            
        return sorted(filtered, key=lambda x: x["score"], reverse=True)
