import os
import pyglet
import json
from pyglet.window import mouse

with open('events.json', 'r', encoding="utf-8") as f:
    events = json.load(f)

active_event = None

# Ablak létrehozása
window_width = 1920  # Ablak szélessége
window_height = 1080  # Ablak magassága
book_width = 700
book_height = 700
window = pyglet.window.Window(width=window_width, height=window_height)

# Háttérkép betöltése
background_path = os.path.join(os.path.dirname(__file__), '..', 'resources', 'images', 'background.png')
background_image = pyglet.image.load(background_path)
background_sprite = pyglet.sprite.Sprite(background_image)
background_sprite.scale = max(book_width / background_sprite.width, book_height / background_sprite.height)
background_sprite.x = (window_width - background_sprite.width) // 2
background_sprite.y = (window_height - background_sprite.height) // 2

# Felső és alsó címkék
upper_text = "Felső szöveg"
desc_text = "Alsó szöveggg"

upper_label = pyglet.text.Label(upper_text,
                                font_name='Arial',
                                font_size=36,
                                x=background_sprite.x + book_width // 2, y=background_sprite.y + book_height * 1.2,
                                anchor_x='center', anchor_y='center', color=(255, 0, 0, 255))

desc_label = pyglet.text.Label(desc_text,
                               font_name='Arial',
                               font_size=20,
                               width=500,
                               x=background_sprite.x + book_width // 2 - 20, y=background_sprite.y + book_height * 1.1,
                               anchor_x='center', anchor_y='center', color=(255, 0, 0, 255), multiline=True)

num_fields = 0
field_height = 0
field_width = 0
field_offset = 0
fields = {}
labels = {}
selected_field = None


def update_event(event_id):
    global active_event
    active_event = next((event for event in events if event['id'] == event_id), None)
    show_active_event()


def show_active_event():
    if active_event:
        eventneve = active_event['name']
        eventleiras = active_event['description']
        upper_label.text = eventneve
        desc_label.text = eventleiras
        create_choices(active_event['choices'])


def create_fields(generatedfieldnumber):
    for i in range(generatedfieldnumber):
        y = field_offset + i * field_height
        field = pyglet.shapes.Rectangle(0, y, field_width, field_height, color=(255, 255, 255, 200))
        field.x = (background_sprite.x + book_width // 2 - field_width // 2)  # Az alsó mezők középre igazítása

        label = pyglet.text.Label(f"{i}. label",
                                  font_name='Arial',
                                  font_size=20,
                                  color=(0, 0, 255, 100),
                                  x=background_sprite.x + book_width // 2,
                                  y=y + field_height // 2,
                                  anchor_x='center', anchor_y='center')

        fields[i] = field
        labels[i] = label


# A választási lehetőségek megjelenítése
def create_choices(choices):
    global fields, labels, num_fields, field_height, field_width, field_offset
    num_fields = len(choices)
    field_height = book_height * 0.8 / num_fields  # Az alsó mezők magassága
    field_width = book_width * 0.8  # Az alsó mezők szélessége
    field_offset = int(book_height * 0.3)  # Az alsó mezők eltolása az ablak tetejétől
    print(field_offset)
    create_fields(num_fields)

    for i, choice in enumerate(choices):
        if i < num_fields:
            labels[i].text = choice['description']

        else:
            break


@window.event
def on_mouse_motion(x, y, dx, dy):
    global selected_field
    helper = None
    for i, field in fields.items():
        if field.x <= x <= field.x + field.width and field.y <= y <= field.y + field.height:
            field.color = (200, 0, 0)
            helper = field
        else:
            field.color = (255, 255, 255)

    if helper is not None:
        selected_field = round((int(helper.y) - int(field_offset)) / int(field_height)) + 1
    else:
        selected_field = None


@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == mouse.LEFT and selected_field:
        print(f"Kiválasztott mező: {selected_field}")

    if button == mouse.LEFT and selected_field == 1:
        window.close()


@window.event
def on_draw():
    window.clear()
    background_sprite.draw()
    upper_label.draw()
    desc_label.draw()
    for field in fields.values():
        field.draw()
    for label in labels.values():
        label.draw()


update_event(3)
pyglet.app.run()
