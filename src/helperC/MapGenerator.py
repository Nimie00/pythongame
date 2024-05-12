import json
import random
import os

import numpy as np


class Tile:
    def __init__(self, terrain):
        self.terrain = terrain


class MapGenerator:
    def __init__(self, width=4, height=4, seed=None):
        self.width = width
        self.height = height
        self.map = [[None for _ in range(width)] for _ in range(height)]
        self.seed = seed

    def generate_basic_map(self):
        np.random.seed(self.seed)
        for i in range(self.height):
            for j in range(self.width):
                self.map[i][j] = Tile("grass")

    def generate_forests(self, num_forests, max_radius):
        np.random.seed(self.seed + 1)
        for _ in range(num_forests):
            x = np.random.randint(max_radius, self.width - max_radius)
            y = np.random.randint(max_radius, self.height - max_radius)
            tiles_placed = 0
            while tiles_placed < max_radius * 2 * np.pi:
                for i in range(-max_radius, max_radius + 1):
                    for j in range(-max_radius, max_radius + 1):
                        if np.random.random() < 1 / (max_radius + 1 - abs(i) + abs(j)):
                            new_x = x + i
                            new_y = y + j
                            if 0 <= new_x < self.width and 0 <= new_y < self.height:
                                if self.map[new_x][new_y].terrain == "grass":
                                    self.map[new_x][new_y] = Tile("forest")
                                    tiles_placed += 1
                max_radius -= 1

    def generate_rivers(self, num_rivers):
        np.random.seed(self.seed + 2)
        print(self.seed)
        for _ in range(num_rivers):
            x = np.random.randint(0, self.width)
            y = np.random.randint(0, self.height)
            self.generate_river(x, y)

    def generate_river(self, x, y):
        np.random.seed(self.seed + 3)
        self.map[x][y] = Tile("river")
        while True:
            direction = self.choose_direction(x, y)  # Choose direction deterministically
            new_x = x + direction[0]
            new_y = y + direction[1]
            if 0 <= new_x < self.width and 0 <= new_y < self.height:
                self.map[new_x][new_y] = Tile("river")
                x, y = new_x, new_y
            else:
                break

    def choose_direction(self, x, y):
        np.random.seed(self.seed ^ x ^ y)  # Deterministic seed based on current position
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        return random.choice(directions)

    def generate_mountains(self, num_mountains, max_radius):
        np.random.seed(self.seed + 4)
        print(self.seed)
        for _ in range(num_mountains):
            x = np.random.randint(max_radius, self.width - max_radius)
            y = np.random.randint(max_radius, self.height - max_radius)
            tiles_placed = 0
            while tiles_placed < max_radius * 2 * np.pi:
                for i in range(-max_radius, max_radius + 1):
                    for j in range(-max_radius, max_radius + 1):
                        if np.random.random() < 1 / (max_radius + 1 - abs(i) + abs(j)):
                            new_x = x + i
                            new_y = y + j
                            if 0 <= new_x < self.width and 0 <= new_y < self.height:
                                if self.map[new_x][new_y].terrain == "grass":
                                    self.map[new_x][new_y] = Tile("mountain")
                                    tiles_placed += 1
                max_radius -= 1

    def generate_cities(self, num_cities, minsize, maxsize):
        np.random.seed(self.seed + 4)
        for _ in range(num_cities):
            x = np.random.randint(0, self.width)
            y = np.random.randint(0, self.height)
            size = np.random.randint(minsize, maxsize)  # Random size for the city
            for i in range(x, min(x + size, self.width)):
                for j in range(y, min(y + size, self.height)):
                    if self.map[i][j].terrain == "grass":
                        self.map[i][j] = Tile("city")

    def save_map(self, filename):
        map_data = {
            "width": self.width,
            "height": self.height,
            "map": [[tile.terrain for tile in row] for row in self.map]
        }
        base_dir = os.path.dirname(os.path.abspath(__file__))  # a jelenlegi fájl helye
        resources_dir = os.path.join(base_dir, 'resources', 'maps')  # a resources/maps mappa elérési útja
        os.makedirs(resources_dir, exist_ok=True)  # létrehozza a mappát, ha még nem létezik
        file_path = os.path.join(resources_dir, filename)  # a teljes fájl elérési útja
        with open(file_path, 'w') as file:
            json.dump(map_data, file)

    def display_map(self):
        color_map = {"grass": "\033[32m", "forest": "\033[33m", "river": "\033[34m", "city": "\033[30m",
                     "mountain": "\033[37m"}
        reset_color = "\033[0m"  # Reset color to default
        for row in self.map:
            for tile in row:
                print(f"{color_map[tile.terrain]}█{reset_color}",
                      end="")  # Change color before printing and reset after
                print()

def generate_map(szelesseg,magassag,seed,mapneve):
    map_generator = MapGenerator(szelesseg, magassag, seed=seed)  # Setting seed for reproducibility
    map_generator.generate_basic_map()
    map_generator.generate_forests(5, 4)
    map_generator.generate_mountains(3, 4)
    map_generator.generate_rivers(2)
    map_generator.generate_cities(5, 1, 5)
    map_generator.save_map(mapneve)
    return map_generator


generate_map()
