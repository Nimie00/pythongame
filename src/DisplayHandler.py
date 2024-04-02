import pyglet

class DisplayHandler:
    def __init__(self):
        self.window = pyglet.window.Window(width=800, height=600)

        # Creating label for displaying log
        self.log_label = pyglet.text.Label(text="Game Log:",
                                           x=10, y=10,
                                           anchor_x='left', anchor_y='bottom')

        # Creating label for displaying current event
        self.event_label = pyglet.text.Label(text="Current Event:",
                                              x=self.window.width // 2, y=self.window.height // 2,
                                              anchor_x='center', anchor_y='center')

        # Creating label for displaying group info
        self.group_label = pyglet.text.Label(text="Group Info:",
                                              x=self.window.width - 10, y=self.window.height - 10,
                                              anchor_x='right', anchor_y='top')

        # Creating label for displaying map
        self.map_label = pyglet.text.Label(text="Map:",
                                            x=10, y=self.window.height - 10,
                                            anchor_x='left', anchor_y='top')

        # Schedule update method to redraw the window
        pyglet.clock.schedule_interval(self.update, 1 / 60)

    def update(self, dt):
        # Clear the window
        self.window.clear()

        # Draw labels
        self.log_label.draw()
        self.event_label.draw()
        self.group_label.draw()
        self.map_label.draw()

    def run(self):
        pyglet.app.run()

# Usage example:

display_handler = DisplayHandler()
display_handler.run()
