import json
import os


class ScoreManager:
    SAVE_FILE = "save.json"

    def __init__(self):
        self.score = 0
        self.best_score = 0

        self.load()

    def add(self, amount):
        self.score += amount

        if self.score > self.best_score:
            self.best_score = self.score
            self.save()

    def load(self):
        if not os.path.exists(self.SAVE_FILE):
            return

        try:
            with open(self.SAVE_FILE, "r") as file:
                data = json.load(file)
                self.best_score = data.get(
                    "best_score",
                    0
                )
        except:
            pass

    def save(self):
        data = {
            "best_score": self.best_score
        }

        with open(self.SAVE_FILE, "w") as file:
            json.dump(data, file)