class Player(object):
    def __init__(self):
        self._email = None
        self._charname = None
        self._room = None
        self._phase = None
        self._phase2 = None
        self._pass1 = None
        self._pass2 = None
        self._race = None
        self._gender = None
        self._type = None
        self._strength = None
        self._agility = None
        self._stamina = None
        self._mana = None

    def get_email(self):
        return self._email

    def set_email(self, value):
        self._email = value

    def get_charname(self):
        return self._charname

    def set_charname(self, value):
        self._charname = value

    def get_room(self):
        return self._room

    def set_room(self, value):
        self._room = value

    def get_phase(self):
        return self._phase

    def set_phase(self, value):
        self._phase = value

    def get_phase2(self):
        return self._phase2

    def set_phase2(self, value):
        self._phase2 = value

    def get_pass1(self):
        return self._pass1

    def set_pass1(self, value):
        self._pass1 = value

    def get_pass2(self):
        return self._pass2

    def set_pass2(self, value):
        self._pass2 = value

    def get_race(self):
        return self._race

    def set_race(self, value):
        self._race = value

    def get_gender(self):
        return self._gender

    def set_gender(self, value):
        self._gender = value

    def get_type(self):
        return self._type

    def set_type(self, value):
        self._type = value

    def get_strength(self):
        return self._strength

    def set_strength(self, value):
        self._strength = value

    def get_agility(self):
        return self._agility

    def set_agility(self, value):
        self._agility = value

    def get_stamina(self):
        return self._stamina

    def set_stamina(self, value):
        self._stamina = value

    def get_mana(self):
        return self._mana

    def set_mana(self, value):
        self._mana = value

