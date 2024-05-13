import os

import pygame

import PopupHandler

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60
IMAGES_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "resources", "images",
                             "items")

def load_item_images(character):
    # Képek betöltése és tárolása az item nevekkel együtt
    item_images = {}
    for row_index, row in enumerate(character.inventory):
        for col_index, item in enumerate(row):
            if item is not None:
                item_name = item  # Feltételezzük, hogy az item maga a neve
                image_path = os.path.join(IMAGES_FOLDER, f"{item_name}.png")
                item_image = pygame.image.load(image_path).convert_alpha()
                item_image = pygame.transform.scale(item_image, (30, 30))  # Kép átméretezése 30x30-as méretre
                item_images[(row_index, col_index)] = item_image
            else:
                image_path = os.path.join(IMAGES_FOLDER, "ures.png")
                item_image = pygame.image.load(image_path).convert_alpha()
                item_image = pygame.transform.scale(item_image, (30, 30))  # Kép átméretezése 30x30-as méretre
                item_images[(row_index, col_index)] = item_image

    return item_images


class Display:

    def __init__(self, screen_width, screen_height):
        self.character_image = None
        self.popup_active = None
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.game_time = 8
        self.health_bar_color = (255, 0, 0)
        self.hunger_bar_color = (0, 255, 0)
        pygame.display.set_caption("My Game")  # A képernyő címe
        pygame.font.init()  # Font inicializálása

        self.clock_font = pygame.font.SysFont(None, 36)  # Betűtípus és méret beállítása

        self.day_cycle_ticks = 0  # Nap/éjszaka ciklus időzítője
        pygame.init()
        self.popup_menu = PopupHandler.PopupMenu(self.screen)
        self.setup_screen("day_village1")

    def setup_screen(self, background_type):
        pygame.font.init()  # Font inicializálása
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("My Game")  # A képernyő címe
        self.screen.fill(BLACK)
        clock = pygame.time.Clock()
        clock.tick(60)
        self.character_image = pygame.image.load(
            os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "resources",
                         "images", "characters", "character.png"))  # Játékos karakter képe
        self.render_background(background_type)

    def update(self, player, time):
        self.game_time = time
        if player is None or player.health <= 0:
            return None
        hunger = player.get_hunger()
        health = player.get_health()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pass
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.popup_active:
                    choice = self.popup_menu.handle_event(event)
                    if choice:
                        self.popup_active = False
                else:
                    self.popup_active = True

        bookwidth = 300
        bookheight = 600
        background_image_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "resources",
                                             "images", "backgrounds", "background.png")
        background_image = pygame.image.load(background_image_path)
        background_image = pygame.transform.scale(background_image, (bookwidth, bookheight))
        background_rect = background_image.get_rect()
        background_rect.bottomright = (self.screen_width, self.screen_height)
        self.screen.blit(background_image, background_rect)

        # Életerő csík kirajzolása
        health_bar_width = health * (bookwidth - 80) / 100
        health_bar_rect = pygame.Rect(900 + bookwidth - health_bar_width - 10, self.screen_height - 70,
                                      health_bar_width, 10)
        pygame.draw.rect(self.screen, self.health_bar_color, health_bar_rect)

        # Éhség csík kirajzolása
        hunger_bar_width = hunger * (bookwidth - 80) / 100
        hunger_bar_rect = pygame.Rect(900 + bookwidth - hunger_bar_width - 10, self.screen_height - 55,
                                      hunger_bar_width, 10)
        pygame.draw.rect(self.screen, self.hunger_bar_color, hunger_bar_rect)

        # Játékos karakter képének megjelenítése a képernyő jobb alsó sarkában
        character_rect = self.character_image.get_rect()
        character_rect.bottomright = (900 + bookwidth - 10, self.screen_height - 70)
        self.screen.blit(self.character_image, character_rect)

        font = pygame.font.SysFont(None, 24)
        text = font.render(f" A vagyonod: {player.money} érme", True, (255, 255, 255))
        text_rect = text.get_rect(center=(1070, 250))
        self.screen.blit(text, text_rect)

        self.draw_item_images(load_item_images(player), 300)  # Az inventory 500 pixellel lentebb legyen elhelyezve

        self.day_cycle_ticks += 1
        if self.day_cycle_ticks >= 24:
            self.day_cycle_ticks = 0

        self.show_clock()

        pygame.display.flip()  # Képernyő frissítése
        return None

    def draw_popup(self):
        self.popup_menu = PopupHandler.PopupMenu(self.screen)
        vissza = self.popup_menu.draw()
        print(vissza)
        return vissza

    def draw_npcshop(self, npc, player):
        self.popup_menu = PopupHandler.PopupMenu(self.screen)
        return self.popup_menu.draw_npc_inventory_menu(npc, player)

    def draw_npcbuys(self, npc, player):
        self.popup_menu = PopupHandler.PopupMenu(self.screen)
        return self.popup_menu.draw_npc_buys_from_player(npc, player)

    def draw_item_images(self, item_images, y_offset):
        for position, item_image in item_images.items():
            self.screen.blit(item_image, (
                self.screen_width - 200 + position[0] * 30, position[1] * 30 + y_offset))  # Elhelyezés a képernyőn
        pygame.display.flip()

    def update_game_time(self):
        # Játékbeli idő frissítése
        self.game_time += 1  # 1 mp-el növeljük az időt minden ciklusban

    def render_background(self, background_type):
        background_image_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "resources",
                                             "images", "backgrounds", background_type + ".jpg")
        background_image = pygame.image.load(background_image_path)
        background_image = pygame.transform.scale(background_image, (self.screen_width, self.screen_height))
        self.screen.blit(background_image, (0, 0))

    def show_clock(self):
        current_time = self.game_time  # Játékbeli idő lekérése

        # Időformátum kialakítása (óra:perc)
        hours = current_time % 24
        days = current_time // 24
        time_str = f"{days:02d}. nap {hours:02d}. óra"

        clock_text = self.clock_font.render(time_str, True, WHITE)
        text_rect = clock_text.get_rect(bottomright=(self.screen_width - 40, self.screen_height - 320))
        self.screen.blit(clock_text, text_rect)
