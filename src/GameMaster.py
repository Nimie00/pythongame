import random

class Event:
    def __init__(self, name, options, event_id, starting_player):
        self.name = name
        self.options = options
        self.event_id = event_id
        self.starting_player = starting_player

class GameInstance:
    def start(self):
        print("Game started!")

class GameMaster:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.game_instance = None
        self.events = []

    def add_event(self, event):
        self.events.append(event)

    def start_game(self):
        if self.game_instance:
            self.game_instance.start()
        else:
            print("No game instance available. Please set the game instance before starting the game.")

    def start_event(self):
        if self.events:
            event = random.choice(self.events)
            print(f"Event: {event.name}")
            print("Options:")
            for i, option in enumerate(event.options, start=1):
                print(f"{i}. {option}")
            print(f"Event ID: {event.event_id}")
            print(f"Starting player: {event.starting_player}")
        else:
            print("No events available. Please add events before starting an event.")

# Usage example:

gm = GameMaster()
gm.game_instance = GameInstance()

# Creating an event
event1 = Event("Battle", ["Attack", "Defend", "Retreat"], 1, "Player 1")
event2 = Event("Treasure Hunt", ["Search", "Leave"], 2, "Player 2")

# Adding events to GameMaster
gm.add_event(event1)
gm.add_event(event2)

# Starting the game
gm.start_game()

# Starting an event
gm.start_event()
