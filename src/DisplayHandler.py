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
day_text = "1"
upper_text = "Felső szöveg"
desc_text = "Alsó szöveggg"

day_label = pyglet.text.Label(day_text,
                              font_name='Arial',
                              font_size=36,
                              x=background_sprite.x + book_width // 2, y=background_sprite.y + book_height * 1.25,
                              anchor_x='center', anchor_y='center', color=(255, 200, 0, 255))

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
globaleventid = 1
selected_field = None


def update_event(event_id):
    global active_event
    active_event = next((event for event in events if event['id'] == event_id), None)
    show_active_event()


def show_active_event():
    global day_text
    if active_event:
        eventneve = active_event['name']
        eventleiras = active_event['description']
        upper_label.text = eventneve
        desc_label.text = eventleiras
        create_choices(active_event['choices'])
    return active_event


def create_fields(generatedfieldnumber, result):
    if not result:
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
    else:
        y = field_offset + 1 * field_height
        field = pyglet.shapes.Rectangle(0, y, field_width, field_height, color=(255, 255, 255, 200))
        field.x = (background_sprite.x + book_width // 2 - field_width // 2)  # Az alsó mezők középre igazítása

        global selected_field, text1
        event = next((event for event in events if event['id'] == 1), None)
        choices = event['choices']
        for choice in choices:
            if choice['id'] == selected_field:
                text1 = choice['result']

        label = pyglet.text.Label("továbblépés",
                                  font_name='Arial',
                                  font_size=20,
                                  color=(0, 0, 255, 100),
                                  x=background_sprite.x + book_width // 2,
                                  y=y + (field_height // 2),
                                  anchor_x='center', anchor_y='center')

        label2 = pyglet.text.Label(text1,
                                   font_name='Arial',
                                   font_size=20,
                                   color=(0, 0, 255, 100),
                                   x=background_sprite.x + book_width // 2,
                                   y=y + (field_height // 2) + 200,
                                   anchor_x='center', anchor_y='center')

        fields['0'] = field
        labels['0'] = label
        labels['1'] = label2


# A választási lehetőségek megjelenítése
def create_choices(choices):
    global fields, labels, num_fields, field_height, field_width, field_offset
    num_fields = len(choices)
    field_height = book_height * 0.8 / num_fields  # Az alsó mezők magassága
    field_width = book_width * 0.8  # Az alsó mezők szélessége
    field_offset = int(book_height * 0.3)  # Az alsó mezők eltolása az ablak tetejétől
    create_fields(num_fields, False)

    for i, choice in enumerate(choices):
        if i < num_fields:
            labels[i].text = choice['description']

        else:
            break


def clearscreen():
    global fields, labels, num_fields
    for field in fields.values():
        print(field)
        field.delete()
        del field
    fields = {}
    for label in labels.values():
        label.delete()
        del label
    labels = {}
    num_fields = 0


def displayresult():
    create_fields(1, True)


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
        clearscreen()
        displayresult()

    if button == mouse.LEFT and selected_field == 2 and len(fields) == 1 and len(labels) == 2:
        global globaleventid, day_text
        day_text = str(int(day_text)+1)
        day_label.text = day_text
        globaleventid += 1
        clearscreen()
        update_event(globaleventid)


@window.event
def on_draw():
    window.clear()
    background_sprite.draw()
    upper_label.draw()
    desc_label.draw()
    day_label.draw()
    for field in fields.values():
        field.draw()
    for label in labels.values():
        label.draw()


update_event(globaleventid)
pyglet.app.run()
