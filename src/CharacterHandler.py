import random


class Character:

    def __init__(self, name, player=False, image_path=None):
        self.name = name
        self.image_path = image_path
        self.health = 100
        self.hunger = 100
        self.player = player
        self.name = name
        self.has_food = 0
        self.activity_probabilities = {
            "Barangolás": 0.25,
            "Állás a standnál": 0.25,
            "Járkálás a falu vásárjában": 0.25,
            "Gyűjtögető üzemmód": 0.25,
        }
        self.activity_durations = {
            "Barangolás": random.randint(1, 3),
            "Állás a standnál": random.randint(2, 5),
            "Járkálás a falu vásárjában": random.randint(3, 7),
            "Gyűjtögető üzemmód": random.randint(4, 8),
            "Alvás": 8
        }
        self.activity = None  # Alapértelmezett tevékenység: Barandolás
        self.stand_at_city = False  # Áll-e a standnál a városban
        self.wandering_at_market = False  # Járkál-e a falu vásárjában
        self.collecting_mode = False  # Gyűjtögető üzemmód
        self.sleeping = False  # Alszik-e éppen
        self.inventory = [[None] * 5 for _ in range(5)]  # 5x5 méretű felszerelés táblázat
        self.money = 30  # Pénz számláló
        self.food_items = {"alma": 40, "hal": 70, "sajt": 60,
                           "eletero_itala": 200, "gyogynoveny": 50}  # Élelmiszerek és visszatöltött életerők táblázata

    def decrease_health(self, value):
        self.health -= value
        if self.health <= 0:
            print("Game Over! Your character has died.")
            # Végrehajtandó lépések a karakter halála eseté

    def decrease_hunger(self, value):
        self.hunger -= value
        if self.hunger <= 0:
            self.decrease_health(3)  # Éhség esetén az életerő csökkenése

    def increase_health(self, value):
        if self.health + value <= 100:  # Az életerő nem lehet 100 fölött
            self.health += value
        else:
            self.health = 100

    def increase_hunger(self, value):
        if self.hunger + value <= 100:  # Az éhség nem lehet 100 fölött
            self.hunger += value
        else:
            v = self.hunger + value
            self.increase_health(v - 100)
            self.hunger = 100

    def add_item_to_inventory_in_order(self, item):
        match item:
            case "alma", "kenyér", "hal", "sajt", "életerő itala" if self.hunger < 30:
                self.eat_food(item)
                item = None
            case _:
                pass

        for row in range(len(self.inventory)):
            for col in range(len(self.inventory[row])):
                if self.inventory[row][col] is None:
                    self.inventory[row][col] = item
                    return

    def remove_item_from_inventory(self, row, col):
        if self.inventory[row][col] is not None:
            item = self.inventory[row][col]
            self.inventory[row][col] = None
        else:
            pass

    def display_inventory(self):
        print("Your Inventory:")
        for row in self.inventory:
            print(row)

    def buy_item(self, item, price):
        if self.money >= price:
            self.money -= price
            print(f"Purchased {item} for {price} money.")
        else:
            print("Not enough money to buy the item.")

    def sell_item(self, position, item, price, seller, buyer):
        seller.remove_item(position)
        buyer.add_item_to_inventory_in_order(item)
        seller.money += price
        buyer.money -= price

    def search_for_item(self):
        pass

    def full_inventory(self):
        for row in range(len(self.inventory)):
            for col in range(len(self.inventory[row])):
                if self.inventory[row][col] is not None:
                    return False
        return True

    def clear_inventory(self):
        for row in range(1):
            for col in range(5):
                self.inventory[row][col] = None

    def eat_food(self, food):
        if food in self.food_items:
            self.increase_hunger(self.food_items[food])
            print(f"Ate {food}.")
        else:
            print(f"{food} is not in the food items list.")

    def change_activity(self, activity):
        self.activity = activity

    def reset_times(self):
        self.activity_durations = {
            "Barangolás": random.randint(3, 4),
            "Állás a standnál": random.randint(3, 5),
            "Járkálás a falu vásárjában": random.randint(3, 7),
            "Gyűjtögető üzemmód": random.randint(3, 5),
            "Alvás": 8
        }

    def sleeps(self):
        self.increase_health(4)

    def perform_daily_activities(self, time):
        if (time > 20 or time < 4) and self.activity != "Alvás":
            self.activity = "Alvás"
            self.activity_durations[self.activity] = 8
        self.activity_durations[self.activity] -= 1

        match self.activity:
            #     case "Barangolás": self.barangol()
            #     case "Állás a standnál": self.standol()
            #     case "Járkálás a falu vásárjában": self.nezelodik()
            #     case "Gyűjtögető üzemmód": self.gyujtoget()
            case "Alvás" if self.activity == "Alvás":
                self.sleeps()
            case _:
                pass

        if self.activity_durations[self.activity] <= 0:
            self.reset_times()
            self.activity = None

    def get_health(self):
        return self.health

    def get_hunger(self):
        return self.hunger

    def remove_item(self, position):
        row, index = position
        self.inventory[row][index] = None

    def try_to_eat(self):
        for row_index, row in enumerate(self.inventory):  # Itt használjuk az enumerate-t a sor indexének meghatározására
            for col_index, item in enumerate(row):
                if item in self.food_items:  # Ellenőrizze, hogy az adott tárgy szerepel-e az élelmiszerek között
                    self.eat_food(item)  # Elfogyasztja az ételt
                    self.remove_item((row_index, col_index))  # Törli az ételt az inventoryból
                    return True
        return False

    def get_name(self):
        return self.name

    def get_image_path(self):
        return self.image_path

    def get_player(self):
        return self.player

    def get_has_food(self):
        return self.has_food

    def get_activity_probabilities(self):
        return self.activity_probabilities

    def get_activity_durations(self):
        return self.activity_durations

    def get_activity(self):
        return self.activity

    def get_stand_at_city(self):
        return self.stand_at_city

    def get_wandering_at_market(self):
        return self.wandering_at_market

    def get_collecting_mode(self):
        return self.collecting_mode

    def get_sleeping(self):
        return self.sleeping

    def get_inventory(self):
        return self.inventory

    def get_money(self):
        return self.money

    def get_food_items(self):
        return self.food_items

        # Setterek

    def set_name(self, name):
        self.name = name

    def set_image_path(self, image_path):
        self.image_path = image_path

    def set_player(self, player):
        self.player = player

    def set_has_food(self, has_food):
        self.has_food = has_food

    def set_activity_probabilities(self, activity_probabilities):
        self.activity_probabilities = activity_probabilities

    def set_activity_durations(self, activity_durations):
        self.activity_durations = activity_durations

    def set_activity(self, activity):
        self.activity = activity

    def set_stand_at_city(self, stand_at_city):
        self.stand_at_city = stand_at_city

    def set_wandering_at_market(self, wandering_at_market):
        self.wandering_at_market = wandering_at_market

    def set_collecting_mode(self, collecting_mode):
        self.collecting_mode = collecting_mode

    def set_sleeping(self, sleeping):
        self.sleeping = sleeping

    def set_inventory(self, inventory):
        self.inventory = inventory

    def set_money(self, money):
        self.money = money

    def set_food_items(self, food_items):
        self.food_items = food_items
