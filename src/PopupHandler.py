import pygame
import sys
import random
import os

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


collectables_values = {
    "kard": random.randint(10, 50),
    "pajzs": random.randint(20, 60),
    "eletero_itala": random.randint(30, 70),
    "arany_kulcs": random.randint(40, 80),
    "arany_erme": random.randint(50, 90),
    "dragako": random.randint(60, 100),
    "alma": random.randint(5, 15),
    "sajt": random.randint(15, 25),
    "hal": random.randint(20, 30),
    "gyogynoveny": random.randint(25, 35),
    "feher_rozsa": random.randint(30, 40),
    None: 0,
    "": 0
}


def find_first_non_empty_slot(inventory):
    for row_index, row in enumerate(inventory):
        for col_index, item in enumerate(row):
            if item is not None:
                return row_index, col_index
    return -1, -1


class PopupMenu:
    def __init__(self, screen):
        self.selected_option = None
        self.menu_active = None
        self.screen = screen
        self.font = pygame.font.SysFont(None, 36)

        self.options = ["Barangol", "Standnál áll", "Járkál a faluban", "Gyűjtöget", "Alszik"]
        self.option_rects = []

        self.width = 200
        self.height = 250
        self.x = (screen.get_width() - self.width) // 2
        self.y = (screen.get_height() - self.height) // 2

        self.bg_color = (255, 255, 255)
        self.text_color = (0, 0, 0)

        pygame.font.init()

    def draw(self):
        # Popup ablak megjelenítése
        self.menu_active = True
        while self.menu_active:
            popup_surface = pygame.Surface((300, 400), pygame.SRCALPHA)  # Átlátszó felület létrehozása
            popup_surface.fill((0, 255, 0, 150))  # Félig átlátszó fehér háttér

            # Szöveg megjelenítése a popup ablak tetején
            font = pygame.font.SysFont(None, 24)
            text = font.render("Válassz egy tevékenységet!", True, (0, 0, 0))
            text_rect = text.get_rect(center=(150, 50))
            popup_surface.blit(text, text_rect)
            # Opciók hozzáadása a popup ablakhoz
            options = ["Barangolás", "Állás a standnál", "Járkálás a falu vásárjában", "Gyűjtögető üzemmód", "Alvás"]
            for i, option in enumerate(options):
                text = font.render(option, True, (0, 0, 0))
                text_rect = text.get_rect(center=(140, 75 + i * 50))

                mouseposx, mouseposy = pygame.mouse.get_pos()
                mouseposx -= 450
                mouseposy -= 200
                if text_rect.collidepoint(mouseposx, mouseposy):
                    text.set_alpha(255)
                else:
                    text.set_alpha(128)  # Az alapértelmezett átlátszóság 50%
                popup_surface.blit(text, text_rect)
                pygame.draw.rect(popup_surface, (255, 255, 255), text_rect, 2)  # Fehér négyzet a tárgy körül

                # Popup ablak kirajzolása a képernyő közepén
            popup_rect = popup_surface.get_rect(center=(600, 400))
            self.screen.blit(popup_surface, popup_rect)

            # Az események figyelése, és a felhasználó választásának visszaadása
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouseposx, mouseposy = pygame.mouse.get_pos()
                    mouseposx -= 450
                    mouseposy -= 200
                    for i, option in enumerate(options):
                        text_rect = pygame.Rect(140, 75 + i * 50, 200, 40)  # Gombok helyének beállítása
                        if text_rect.collidepoint(mouseposx, mouseposy):
                            self.menu_active = False  # A menü bezárása
                            self.selected_option = option
                            return self.selected_option

            pygame.display.flip()

    def draw_npc_buys_from_player(self, npc, player):
        # Kiválasztunk egy random itemet az npc-től
        slotx, sloty = find_first_non_empty_slot(player.inventory)
        if (slotx, sloty) == (-1, -1):
            return None
        item_name = player.inventory[slotx][sloty]
        item_price = collectables_values[item_name] + random.randint(-11, 10)

        # Popup ablak megjelenítése
        self.menu_active = True
        while self.menu_active:
            popup_surface = pygame.Surface((300, 400), pygame.SRCALPHA)  # Átlátszó felület létrehozása
            popup_surface.fill((255, 255, 255, 200))  # Félig átlátszó fehér háttér

            # Szöveg megjelenítése a popup ablak tetején
            font = pygame.font.SysFont(None, 24)
            text = font.render("NPC Buys Item", True, (0, 0, 0))
            text_rect = text.get_rect(center=(150, 25))
            popup_surface.blit(text, text_rect)

            # A random item megjelenítése és az árának kiírása
            item_image_path = os.path.join(IMAGES_FOLDER, f"{item_name}.png")
            item_image = pygame.image.load(item_image_path).convert_alpha()
            item_image = pygame.transform.scale(item_image, (100, 100))  # Kép átméretezése 100x100-as méretre
            item_rect = item_image.get_rect(center=(150, 150))
            popup_surface.blit(item_image, item_rect)

            price_text = font.render(f"Price: {item_price}", True, (0, 0, 0))
            price_rect = price_text.get_rect(midtop=(item_rect.centerx, item_rect.bottom))
            popup_surface.blit(price_text, price_rect)

            # Igen és Nem gombok megjelenítése
            yes_text = font.render("Yes", True, (0, 0, 0))
            yes_rect = yes_text.get_rect(midtop=(popup_surface.get_width() // 4, 300))
            popup_surface.blit(yes_text, yes_rect)

            no_text = font.render("No", True, (0, 0, 0))
            no_rect = no_text.get_rect(midtop=(popup_surface.get_width() * 3 // 4, 300))
            popup_surface.blit(no_text, no_rect)

            # Popup ablak kirajzolása a képernyő közepén
            popup_rect = popup_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
            self.screen.blit(popup_surface, popup_rect)

            # Az események figyelése, és a menü bezárása
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouseposx, mouseposy = pygame.mouse.get_pos()
                    mouseposx -= 450
                    mouseposy -= 200
                    if yes_rect.collidepoint(mouseposx, mouseposy):
                        player.sell_item((slotx, sloty), item_name, item_price, player, npc)
                        self.menu_active = False
                    elif no_rect.collidepoint(mouseposx, mouseposy):
                        self.menu_active = False

            pygame.display.flip()

    def draw_npc_inventory_menu(self, npc, player):
        # Popup ablak megjelenítése
        self.menu_active = True
        while self.menu_active:
            popup_surface = pygame.Surface((300, 400), pygame.SRCALPHA)  # Átlátszó felület létrehozása
            popup_surface.fill((0, 255, 0, 200))  # Félig átlátszó fehér háttér

            # Szöveg megjelenítése a popup ablak tetején
            font = pygame.font.SysFont(None, 24)
            text = font.render(f"{npc.name} Tárgyai:", True, (0, 0, 0))
            text_rect = text.get_rect(center=(150, 25))
            popup_surface.blit(text, text_rect)

            # NPC által tárolt tárgyak képeinek betöltése
            item_images = load_item_images(npc)

            # NPC által tárolt tárgyak képeinek megjelenítése
            for position, item_image in item_images.items():
                row_index, col_index = position
                image_rect = item_image.get_rect(topleft=(50 + col_index * 40, 50 + row_index * 40))
                popup_surface.blit(item_image, image_rect)

                # Fehér négyzet hozzáadása a tárgy hitboxához
                pygame.draw.rect(popup_surface, (255, 255, 255), image_rect, 2)  # Fehér négyzet a tárgy körül

                # Ha az egér a tárgy fölé kerül, akkor jelenjen meg az ár
                mouseposx, mouseposy = pygame.mouse.get_pos()
                mouseposx -= 450
                mouseposy -= 200
                if image_rect.collidepoint(mouseposx, mouseposy):
                    item_name = npc.inventory[row_index][col_index]
                    item_price = collectables_values[item_name]
                    price_text = font.render(f"Price: {item_price}", True, (0, 0, 0))
                    price_rect = price_text.get_rect(midtop=image_rect.midbottom)
                    popup_surface.blit(price_text, price_rect)

            # Bezárás gomb megjelenítése
            close_text = font.render("Close", True, (0, 0, 0))
            close_rect = close_text.get_rect(midtop=(popup_surface.get_width() // 2, 350))
            popup_surface.blit(close_text, close_rect)

            # Popup ablak kirajzolása a képernyő közepén
            popup_rect = popup_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
            self.screen.blit(popup_surface, popup_rect)

            # Az események figyelése, és a menü bezárása
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouseposx, mouseposy = pygame.mouse.get_pos()
                    mouseposx -= 450
                    mouseposy -= 200
                    if close_rect.collidepoint(mouseposx, mouseposy):
                        self.menu_active = False
                    for position, item_image in item_images.items():
                        if item_image.get_rect(topleft=(50 + position[1] * 40, 50 + position[0] * 40)).collidepoint(mouseposx, mouseposy):
                            item_name = npc.inventory[position[0]][position[1]]
                            item_price = collectables_values[item_name]
                            if player.money >= item_price and item_name is not None:
                                npc.sell_item(position, item_name, item_price, npc, player)
                                self.menu_active = False
                            else:
                                self.menu_active = False

            pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i, rect in enumerate(self.option_rects):
                if rect.collidepoint(event.pos):
                    return self.options[i]
        return None
