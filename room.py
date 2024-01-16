import threading
class Room(object):
    def __init__(self):
        self._name = None
        self._description = None
        self._directions = None
        self._directions_status = None
        self._items = None
        self._players = None

    # Getter and setter for 'name'
    def get_name(self):
        return self._name

    def set_name(self, value):
        self._name = value

    # Getter and setter for 'description'
    def get_description(self):
        return self._description

    def set_description(self, value):
        self._description = value

    # Getter and setter for 'directions'
    def get_directions(self):
        return self._directions

    def set_directions(self, value):
        self._directions = value

    # Getter and setter for 'directions_status'
    def get_directions_status(self):
        return self._directions_status

    def set_directions_status(self, value):
        self._directions_status = value

    # Getter and setter for 'items'
    def get_items(self):
        return self._items

    def add_item(self, item):
        with self._lock:
            if self._items is None:
                self._items = []
            self._items.append(item)

    # Remove an item from the room with mutual exclusion
    def remove_item(self, item):
        with self._lock:
            if self._items is not None and item in self._items:
                self._items.remove(item)

    # Getter and setter for 'players'
    def get_players(self):
        return self._players

    def add_player(self, player):
        with self._players_lock:
            if self._players is None:
                self._players = []
            self._players.append(player)
    def remove_player(self, player):
        with self._players_lock:
            if self._players is not None and player in self._players:
                self._players.remove(player)