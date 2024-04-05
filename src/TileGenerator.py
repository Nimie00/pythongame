from PIL import Image
import numpy as np

def generate_tile(color, width, height, name):
    # Készítsünk egy üres képet a megadott szélesség és magasság alapján
    img = Image.new('RGBA', (width, height), color=color)

    # Adjunk hozzá egy 1px széles fekete sávot a kép szélén
    img_data = np.array(img)
    img_data[:, :1] = (0, 0, 0, 255)  # Fekete sáv az img bal szélén
    img_data[:, -1:] = (0, 0, 0, 255)  # Fekete sáv az img jobb szélén
    img_data[:1, :] = (0, 0, 0, 255)  # Fekete sáv az img tetején
    img_data[-1:, :] = (0, 0, 0, 255)  # Fekete sáv az img alján

    # Állítsuk be az új adatokat a képen
    img = Image.fromarray(img_data)

    # Mentsük el a képet
    img.save(f'{name}.png')

if __name__ == "__main__":
    generate_tile((175, 65, 84, 255), 32, 32, "mountain")
