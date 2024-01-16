#!/usr/bin/env python

"""A simple Multi-User Dungeon (MUD) game. Players can talk to each
other, examine their surroundings and move between rooms.

Some ideas for things to try adding:
    * More rooms to explore
    * An 'emote' command e.g. 'emote laughs out loud' -> 'Mark laughs
        out loud'
    * A 'whisper' command for talking to individual players
    * A 'shout' command for yelling to players in all rooms
    * Items to look at in rooms e.g. 'look fireplace' -> 'You see a
        roaring, glowing fire'
    * Items to pick up e.g. 'take rock' -> 'You pick up the rock'
    * Monsters to fight
    * Loot to collect
    * Saving players accounts between sessions
    * A password login
    * A shop from which to buy items

author: Mark Frimston - mfrimston@gmail.com
"""

import time

import hashlib
from player import Player
from room import Room
import json
game_name = "MUD LAND"


def start_menu():
    return "********** Welcome Adventurer **********\n" + \
        "**********   Choose  Wisely   **********\n" + \
        "signup\n" + \
        "login\n" + \
        "exit\n"

def logged_in():
    return "************ Welcome Adventurer **********\n" + \
           "********** To the fantastic world **********\n" + \
           "********** of {} **********\n".format(game_name)
        # import the MUD server class
from mudserver import MudServer

def import_rooms(rooms):
    with open("rooms.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            name, description, directions = line.split("|")
            tmp_room=Room()
            tmp_room.set_name(name)
            tmp_room.set_description(description)
            tmp_room.set_directions(json.loads(directions))
            rooms[name] = tmp_room


# structure defining the rooms in the game. Try adding more rooms to the game!
rooms = {}
import_rooms(rooms)
#print (rooms[0].get_name())

# stores the players in the game
players = {}

# start the server
mud = MudServer()

def signup(id, command):
    if players[id].get_phase2()=="Pre-Login":
        mud.send_message(id, "Enter email address: ")
        return "signup1"
    elif players[id].get_phase2()=="signup1":
        players[id].set_email(command)
        mud.send_message(id, "Enter password: ")
        print (players[id].get_email())
        return "signup2"
    elif players[id].get_phase2()=="signup2":
        enc=command.encode()
        passwd = hashlib.md5(enc).hexdigest()
        players[id].set_pass1(passwd)
        mud.send_message(id, "Confirm password: ")
        print (players[id].get_pass1())
        return "signup3"
    elif players[id].get_phase2()=="signup3":
        enc = command.encode()
        passwd = hashlib.md5(enc).hexdigest()
        players[id].set_pass2(passwd)
        if players[id].get_pass2() != players[id].get_pass1():
            mud.send_message(id, "Passwords do not match.\nEnter Password:")
            return "signup2"
        mud.send_message(id, "Insert Character Name: ")
        return "signup4"
    elif players[id].get_phase2() == "signup4":
        players[id].set_charname(command)
        with open("credentials.txt", "a") as f:
                f.write(players[id].get_email() + ":")
                f.write(players[id].get_charname() + ":")
                f.write(players[id].get_pass1() + "\n")
                f.close()
                mud.send_message(id,"You have registered successfully!")

        return "signupend"



def login(id, command):
    if players[id].get_phase2() == "registered1":
        mud.send_message(id, "Enter email address to Login: ")
        return "registered2"
    elif players[id].get_phase2() == "registered2":
        players[id].set_email(command)
        mud.send_message(id, "Enter password to Login: ")
        return "registered3"
    elif players[id].get_phase2() == "registered3":
        enc = command.encode()
        players[id].set_pass1(hashlib.md5(enc).hexdigest())
        user_ok = False
        with open("credentials.txt", "r") as f:
            lines = f.readlines()
            for line in lines:
                stored_email, charname, stored_pwd = line.split(":")
                if players[id].get_email() == stored_email:
                    user_ok = True
                    stored_pwd = stored_pwd.replace("\n", "")
                    break
            f.close()
            if user_ok and players[id].get_pass1() == stored_pwd:
                mud.send_message(id, "{} logged in Successfully!".format(charname))
                players[id].set_charname(charname)
                return "registeredend"
            else:
                mud.send_message(id, "Login Failed!")
                return "registered1"


# main game loop. We loop forever (i.e. until the program is terminated)
while True:

    # pause for 1/5 of a second on each loop, so that we don't constantly
    # use 100% CPU time
    time.sleep(0.2)

    # 'update' must be called in the loop to keep the game running and give
    # us up-to-date information
    mud.update()

    # go through any newly connected players
    for id in mud.get_new_players():
        # add the new player to the dictionary, noting that they've not been
        # named yet.
        # The dictionary key is the player's id number. We set their room to
        # None initially until they have entered a name
        # Try adding more player stats - level, gold, inventory, etc
        players[id] = Player()

        # send the new player a prompt for their name
        mud.send_message(id, start_menu())
        # mud.send_message(id, "What is your name?")

    # go through any recently disconnected players
    for id in mud.get_disconnected_players():

        # if for any reason the player isn't in the player map, skip them and
        # move on to the next one
        if id not in players:
            continue

        # go through all the players in the game
        for pid, pl in players.items():
            # send each player a message to tell them about the disconnected
            # player
            mud.send_message(pid, "{} quit the game".format(players[id].get_charname()))

        # remove the player's entry in the player dictionary
        del (players[id])

    # go through any new commands sent from players
    for id, command, params in mud.get_commands():

        # if for any reason the player isn't in the player map, skip them and
        # move on to the next one
        if id not in players:
            continue

        # if the player hasn't given their name yet, use this first command as
        # their name and move them to the starting room.
        if players[id].get_charname() is None:

            if command == "exit":
                mud._handle_disconnect(id)
            elif command == "signup" or  players[id].get_phase() == "Pre-Login":
                players[id].set_phase("Pre-Login")
                if players[id].get_phase2() is None:
                    players[id].set_phase2("Pre-Login")
                players[id].set_phase2(signup(id, command))
                if players[id].get_phase2() == "signupend":
                    players[id] = Player()
                    players[id].set_phase("Registered")
                    players[id].set_phase2("registered1")
                    mud.send_message(id, start_menu())
            elif command == "login" or  players[id].get_phase() == "Registered":
                players[id].set_phase("Registered")
                if players[id].get_phase2() is None:
                    players[id].set_phase2("registered1")
                players[id].set_phase2(login(id, command))
                if players[id].get_phase2() == "registeredend":

                    players[id].set_phase("Game")
                    players[id].set_phase2(None)
                    mud.send_message(id, logged_in())
                    players[id].set_phase(None)
                    players[id].set_room("Tavern")

                    # go through all the players in the game
                    for pid, pl in players.items():
                        # send each player a message to tell them about the new player
                        mud.send_message(pid, "{} entered the game".format(
                            players[id].get_charname()))

                    # send the new player a welcome message
                    mud.send_message(id, "Welcome to the game, {}. ".format(
                        players[id].get_charname())
                                     + "Type 'help' for a list of commands. Have fun!")

                    # send the new player the description of their current room
                    mud.send_message(id, rooms[players[id].get_room()].get_description())

        # each of the possible commands is handled below. Try adding new
        # commands to the game!

        # 'help' command
        elif command == "help":

            # send the player back the list of possible commands
            mud.send_message(id, "Commands:")
            mud.send_message(id, "  say <message>  - Says something out loud, "
                             + "e.g. 'say Hello'")
            mud.send_message(id, "  look           - Examines the "
                             + "surroundings, e.g. 'look'")
            mud.send_message(id, "  go <exit>      - Moves through the exit "
                             + "specified, e.g. 'go outside'")
            mud.send_message(id, "  leave          - Leave the game without saving."
                             )

        # 'say' command
        elif command == "say":

            # go through every player in the game
            for pid, pl in players.items():
                # if they're in the same room as the player
                if players[pid].getroom() == players[id].get_room():
                    # send them a message telling them what the player said
                    mud.send_message(pid, "{} says: {}".format(
                        players[id].get_charname(), params))

        # 'look' command
        elif command == "look":

            # store the player's current room
            rm = rooms[players[id].get_room()]

            # send the player back the description of their current room
            mud.send_message(id, rm.get_description())

            playershere = []
            # go through every player in the game
            for pid, pl in players.items():
                # if they're in the same room as the player
                if players[pid].get_room() == players[id].get_room():
                    # ... and they have a name to be shown
                    if players[pid].get_charname() is not None:
                        # add their name to the list
                        playershere.append(players[pid].get_charname())

            # send player a message containing the list of players in the room
            mud.send_message(id, "Players here: {}".format(
                ", ".join(playershere)))

            # send player a message containing the list of exits from this room
            mud.send_message(id, "Exits are: {}".format(
                ", ".join(rm.get_directions())))

        # 'go' command
        elif command == "leave":
            mud._handle_disconnect(id)
        elif command == "go":

            # store the exit name
            ex = params.lower()

            # store the player's current room
            rm = rooms[players[id].get_room()]

            # if the specified exit is found in the room's exits list
            if ex in rm.get_directions():

                # go through all the players in the game
                for pid, pl in players.items():
                    # if player is in the same room and isn't the player
                    # sending the command
                    if players[pid].get_room() == players[id].get_room() \
                            and pid != id:
                        # send them a message telling them that the player
                        # left the room
                        mud.send_message(pid, "{} left via exit '{}'".format(
                            players[id].get_charname(), ex))

                # update the player's current room to the one the exit leads to
                players[id].set_room(rm.get_directions()[ex])
                rm = rooms[players[id].get_room()]

                # go through all the players in the game
                for pid, pl in players.items():
                    # if player is in the same (new) room and isn't the player
                    # sending the command
                    if players[pid].get_room() == players[id].get_room() \
                            and pid != id:
                        # send them a message telling them that the player
                        # entered the room
                        mud.send_message(pid,
                                         "{} arrived via exit '{}'".format(
                                             players[id].get_charname(), ex))

                # send the player a message telling them where they are now
                mud.send_message(id, "You arrive at '{}'".format(
                    players[id].get_room()))

            # the specified exit wasn't found in the current room
            else:
                # send back an 'unknown exit' message
                mud.send_message(id, "Unknown exit '{}'".format(ex))

        # some other, unrecognised command
        else:
            # send back an 'unknown command' message
            mud.send_message(id, "Unknown command '{}'".format(command))
