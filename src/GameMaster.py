import time
import random
import pygame
import os

import CharacterHandler
import DailyActivitiesManager as dm
import DisplayHandler as display


class GameMaster:
    def __init__(self):
        self.win = False
        self.met_characters = {}  # A már találkozott karakterek tárolása: {character_name: reputation}
        self.current_time = {"days": 0, "hours": 8}  # A játékbeli idő kezdeti beállítása
        self.characters = []
        self.started = False
        self.player_character = CharacterHandler.Character("Player Character", True, "player_character.jpg")
        self.activities_handler = None
        self.screen = None
        self.background = "day_village1"
        self.shopping = None

    def encounter_character(self, character_name):
        if character_name not in self.met_characters:
            self.met_characters[character_name] = 0  # Új karakter hozzáadása a tárolóhoz
        # Itt lenne az interakció a karakterrel, ami változtatja a reputációt

    def increase_reputation(self, character_name):
        if character_name in self.met_characters:
            self.met_characters[character_name] += 1  # Növeljük a reputációt

    def decrease_reputation(self, character_name):
        if character_name in self.met_characters:
            self.met_characters[character_name] -= 1  # Csökkentjük a reputációt

    def display_met_characters(self):
        print("Met characters:")
        for character, reputation in self.met_characters.items():
            print(f"{character}: {reputation}")

    def time_tick(self):
        self.current_time["hours"] += 1
        if self.current_time["hours"] >= 24:
            self.current_time["days"] += 1
            self.current_time["hours"] = 0

    def display_current_time(self):
        print(f"Current time: Day {self.current_time['days']}, Hour {self.current_time['hours']}")

    def start_game(self):
        self.create_characters()
        self.set_activities()
        self.run_game()
        self.started = True

    def setup_screen(self):
        self.screen = display.Display(1200, 800)
        self.screen.setup_screen("day_village1")

    def set_activities(self):
        ah = dm.DailyActivitiesManager()
        self.activities_handler = ah

    def create_characters(self):
        for i in range(7):
            character = CharacterHandler.Character(f"NPC {i}", f"npc_{i}.jpg")
            self.characters.append(character)

    def run_game(self):
        self.player_character.decrease_hunger(random.randint(2, 5))
        if self.player_character.hunger <= 0:
            self.player_character.decrease_health(3)

        if self.player_character.get_health() <= 0:
            self.player_character = None
            self.started = None

        if self.started:
            text = "day_"
            max_choice = 5

            if self.current_time["hours"] > 16:
                text = "night_"
                max_choice = 2

            choice = self.player_character.activity
            if choice == "Barangolás":
                text += "wonder" + str(random.randint(1, max_choice))
            elif choice == "Állás a standnál":
                text += "sell1"
            elif choice == "Járkálás a falu vásárjában":
                text += "village" + str(random.randint(1, max_choice))
            elif choice == "Gyűjtögető üzemmód":
                text += "wonder" + str(random.randint(1, max_choice))
            elif choice == "Alvás":
                self.background = "sleep"

            if self.background == "":
                self.background = text

            if self.player_character.activity is None:
                self.player_character.activity = self.screen.draw_popup()

                text = "day_"
                max_choice = 5

                if self.current_time["hours"] > 16:
                    text = "night_"
                    max_choice = 2

                choice = self.player_character.activity
                if choice == "Barangolás":
                    text += "wonder" + str(random.randint(1, max_choice))
                elif choice == "Állás a standnál":
                    text += "sell1"
                elif choice == "Járkálás a falu vásárjában":
                    text += "village" + str(random.randint(1, max_choice))
                elif choice == "Gyűjtögető üzemmód":
                    text += "wonder" + str(random.randint(1, max_choice))
                elif choice == "Alvás":
                    self.background = "sleep"

                if self.background == "":
                    self.background = text
                print(
                    f"Player: {self.player_character.activity} -"
                    f" {self.player_character.activity_durations[self.player_character.activity]} óra")

            else:
                print(
                    f"Player: {self.player_character.activity} -"
                    f" {self.player_character.activity_durations[self.player_character.activity]} óra")
                self.player_character.perform_daily_activities(self.current_time['hours'])

                if self.player_character.activity == "Gyűjtögető üzemmód":
                    random_item = random.choice(self.activities_handler.collectables)
                    self.player_character.add_item_to_inventory_in_order(random_item)

                if self.player_character.activity == "Alvás":
                    self.screen.render_background("sleep")

                if self.player_character.hunger < 30:
                    self.player_character.try_to_eat()

            self.screen.render_background(self.background)

            for npc in self.characters:
                if npc.full_inventory():
                    npc.clear_inventory()
                npc.decrease_hunger(random.randint(2, 5))
                if npc.hunger < 30:
                    npc.try_to_eat()
                if npc.hunger <= 0:
                    npc.decrease_health(3)
                if npc.get_activity() is None:
                    npc_activity = self.activities_handler.choose_activity(npc)
                    npc.change_activity(npc_activity)
                    print(f"{npc.name}: {npc_activity} - {npc.activity_durations[npc_activity]} óra")

                else:
                    npc_activity = npc.get_activity()
                    print(f"{npc.name}: {npc_activity} - {npc.activity_durations[npc_activity]} óra")
                    npc.perform_daily_activities(self.current_time["hours"])
                    if npc_activity == "Barangolás":
                        self.increase_reputation(npc.name)
                    elif npc_activity == "Állás a standnál":
                        if self.player_character.activity in ["Járkálás a falu vásárjában"] and random.random() < 0.3:
                            self.shopping = npc
                    elif npc_activity == "Járkálás a falu vásárjában":
                        if self.player_character.activity in ["Állás a standnál"] and random.random() > 0.3:
                            self.player_encounters_market(npc)
                    elif npc_activity == "Gyűjtögető üzemmód":
                        random_item = random.choice(self.activities_handler.collectables)
                        npc.add_item_to_inventory_in_order(random_item)

                if npc.get_health() <= 0:
                    self.characters.remove(npc)

            print("\n")

    def player_interacts_with_stand(self, npc):
        print(f"A {npc.name} standjánál van a játékos, és kereskedik.")
        self.screen.draw_npcshop(npc, self.player_character)

    def player_encounters_market(self, npc):
        print("A játékos a falu vásárjában találkozik más karakterekkel.")
        self.screen.draw_npcbuys(npc, self.player_character)

    def check_win(self):
        if self.player_character.money > 5000:
            self.win = True


if __name__ == "__main__":
    game = GameMaster()
    game.setup_screen()
    game.start_game()

    music_files = ["music (1).ogg", "music (2).ogg", "music (3).ogg"]
    MUSIC_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "resources",
                                "music")

    music_file = os.path.join(MUSIC_FOLDER, random.choice(music_files))
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.1)

    timerino = 8
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if game.started:
            game.time_tick()
            game.run_game()
            game.display_current_time()
            game.check_win()
            time.sleep(1)

            # Képernyő frissítése a játékos életerejével és éhségével
            timerino += 1
            game.screen.update(game.player_character, timerino)
            if not game.started:
                pygame.mixer.stop()
                print("A játék befejeződött")
                if game.win:
                    print("Nyertél")
                else:
                    print("Sajnos nem nyertél")
                break

            if game.player_character.activity is None:
                game.background = ""
                game.player_character.activity = game.screen.draw_popup()

            if game.shopping is not None:
                game.player_interacts_with_stand(game.shopping)
                game.shopping = None
