import pyglet
import json
import sys

class GameWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.drawn = False
        self.batch = pyglet.graphics.Batch()

        self.textures = {
            "grass": pyglet.resource.image('grass.png'),
            "forest": pyglet.resource.image("forest.png"),
            "river": pyglet.resource.image("river.png"),
            "city": pyglet.resource.image("city.png"),
            "mountain": pyglet.resource.image("mountain.png")
        }

        # Betöltjük a térképet a terkep.json fájlból
        with open("../resources/maps/map1", "r") as f:
            self.map_data = json.load(f)


    def update(self, dt):
        self.clear()

        map_width = self.map_data['width']
        map_height = self.map_data['height']

        for y in range(map_height):
            for x in range(map_width):
                tile_info = self.map_data['map'][y][x]

                texture = self.textures[tile_info]

                tile_x = x * texture.width
                tile_y = self.height - (y + 1) * texture.height
                texture.batch = self.batch
                texture.blit(tile_x, tile_y)

if __name__ == "__main__":
    window = GameWindow(1500, 800, "Tile Map")
    pyglet.clock.schedule_interval(window.update, 1 / 1)
    pyglet.app.run()
