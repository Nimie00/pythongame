import random


class DailyActivitiesManager:
    def __init__(self):
        self.characters = []
        self.collectables = [
            "kard",
            "pajzs",
            "eletero_itala",
            "arany_kulcs",
            "arany_erme",
            "dragako",
            "alma",
            "sajt",
            "hal",
            "gyogynoveny",
            "feher_rozsa",
        ]

    def output_characters(self):
        return self.characters

    def choose_activity(self, character):
        chosen_activity = random.choice(list(character.activity_probabilities.keys()))
        character.activity = chosen_activity
        return chosen_activity

    def apply_activity_changes(self):
        for character in self.characters:
            for activity, prob in character.activity_probabilities.items():
                if prob != 0:
                    # Random változás az aktivitások valószínűségében
                    character.activity_probabilities[activity] += random.uniform(-0.1, 0.1)
                    # Korlátozzuk a valószínűségeket 0 és 1 közé
                    character.activity_probabilities[activity] = max(0,
                                                                     min(1, character.activity_probabilities[activity]))
