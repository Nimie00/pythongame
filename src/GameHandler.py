import json
import random

class GameHandler:
    def __init__(self):
        self.day = 1  # Az aktuális nap száma
        self.time_of_day = 0  # Az aktuális napszak (0-5: 0-3: nap, 4-5: éjszaka)
        self.party = []  # A játékos csoportját tartalmazó lista
        self.events = []  # Az eseményeket tartalmazó lista

    def load_events(self, filename):
        # Betölti az eseményeket a JSON fájlból
        with open(filename, 'r', encoding='utf8') as f:
            self.events = json.load(f)

    def start_game(self):
        # Kezdeti beállítások inicializálása
        self.load_events('events.json')
        # Események betöltése

        # Játék indítása
        while True:
            self.process_time()
            self.display_status()
            self.handle_event()

    def process_time(self):
        # Idő folyamatának kezelése
        self.time_of_day += 1
        if self.time_of_day == 6:
            self.time_of_day = 0
            self.day += 1

    def display_status(self):
        # Játék állapotának megjelenítése
        print(f"Nap {self.day}, Időszak: {'Nap' if self.time_of_day < 4 else 'Éjszaka'}")

    def handle_event(self):
        # Esemény kezelése
        event = random.choice(self.events)
        print("\n" + event['name'])
        print(event['description'])
        print("Választási lehetőségek:")
        for i, choice in enumerate(event['choices'], 1):
            print(f"{i}: {choice['description']}")

        choice = int(input("Válassz egy lehetőséget: "))
        while choice < 1 or choice > len(event['choices']):
            print("Érvénytelen választás. Kérem, válasszon újra.")
            choice = int(input("Válassz egy lehetőséget: "))

        # Esemény választásának feldolgozása
        chosen_event = event['choices'][choice - 1]
        print(chosen_event['result'])

if __name__ == "__main__":
    game = GameHandler()
    game.start_game()
