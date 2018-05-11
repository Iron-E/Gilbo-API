# Gilbo RPG API -- Version 0.13.0-alpha2 #

from abc import ABC, abstractmethod
from enum import IntEnum, auto

# Allow Gilbo to see Dependencies
import sys
sys.path.append('./deps/')

# 3rd Party Libraries
import numpy as np
from dispatcher import Signal

# ascii-table.com/ansi-escape-sequences.php
# https://docs.djangoproject.com/en/2.0/topics/signals/#django.contrib.auth.signals.Signal

#
# Events #
#

# Inventory-related
pub_item_obtained = Signal(providing_args=["itms"])
pub_stat_change = Signal(providing_args=["changes"])

# Entity-position-related
pub_chk_pos = Signal()

#
# Common Enumerators #
#


class Enumerators(IntEnum):
    # Inventory enums
    items_to_modify = 1
    infinite_coin = -1
    # Attack enums
    base_ammo_cost = 1
    times_attacking = 1


#
# Functions #
#


def write(phrase, type_speed=.040, line_delay=.5):
    from time import sleep
    if isinstance(phrase, list) or isinstance(phrase, tuple):
        for i in range(len(phrase)):
            for j in range(len(phrase[i])):
                print(phrase[i][j], end="", flush=True)
                sleep(type_speed)

            sleep(line_delay)
            print('', end=' ')
    else:
        for i in range(len(phrase)):
            print(phrase[i], end="", flush=True)
            sleep(type_speed)

        sleep(line_delay)
        print('', end=' ')

    print('\n')


def clr_console():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')


def debug_info(err, more_info, display=False):
    if display is True:
        print(str(more_info), end=" See 'log.txt' for details.\n\n")

    with open('log.txt', 'a') as handle:
        from datetime import datetime
        print(str(datetime.now()), end=':\n', file=handle)
        print(str(err), file=handle)
        print(str(more_info), end='\n\n', file=handle)

#
# Abstract class from which all enemies, NPCs, and players are derived. #
#


class Locate_Entity(IntEnum):
    mapid = 0
    coordinates = 1
    x_cord = 1
    y_cord = 0


class entity(ABC):
    def __init__(self, name, location, x, y):
        self.entity_dict = {'name': name}
        self.entity_dict.update({'location': [location]})
        self.entity_dict['location'].append([y, x])

    @property
    def name(self):
        return self.entity_dict['name']

    @name.setter
    def name(self, value):
        self.entity_dict['name'] = value

    @property
    def location(self):
        return self.entity_dict['location']

    def set_loc(self, cord, location=None):
        if location is None:
            location = self.location[Locate_Entity.mapid.value]

        self.entity_dict['location'][Locate_Entity.mapid.value] = location
        self.entity_dict['location'][Locate_Entity.coordinates.value] = cord


class NPC(entity):
    def __init__(self, name, location, x, y):
        super().__init__(name, location, x, y)
        self.dialogue_dict = {}

    def add_dialogue(self, diag_name, diag_content):
        self.dialogue_dict.update({diag_name: diag_content})

    def say(self, diag_name):
            write(self.dialogue_dict[diag_name])


class vendor(entity):
    def __init__(self, name, location, x, y, inv):
        super().__init__(name, location, x, y)
        self.entity_dict['inventory'] = inv

    @property
    def collection(self):
        return self.entity_dict['inventory']


class battler(vendor):
    def __init__(self, name, location, x, y, inv, stats):
        super().__init__(name, location, x, y, inv)
        self.entity_dict['stats'] = stats

        def handle_stat_change(sender, **kwargs):
            self.sub_stat_change(sender, **kwargs)
        self.handle_stat_change = handle_stat_change
        pub_stat_change.connect(handle_stat_change)

    @property
    def stats(self):
        return self.entity_dict['stats']

    @property
    def attacks(self):
        try:
            for itm in self.collection.equipped:
                if isinstance(itm, weapon):
                    return itm.linked_attacks
        except AttributeError as e:
            debug_info(e, 'The battler must use a battler_collection for an inventory.', True)

    def sub_stat_change(self, sender, **kwargs):
        if sender is self.collection:
            self.stats.stat_list = kwargs['changes']


class player(battler):
    def __init__(self, name, location, x, y, inv, stats):
        super().__init__(name, location, x, y, inv, stats)

        self.entity_dict['quest_list'] = []

        def handle_chk_pos(sender, **kwargs):
            self.sub_chk_pos(sender, **kwargs)
        self.handle_chk_pos = handle_chk_pos
        pub_chk_pos.connect(handle_chk_pos)

    # @receiver(pub_chk_pos)
    def sub_chk_pos(self, sender, **kwargs):
        sender.player_pos = self.location

#
# Items/Weapons in the game #
#


class Item_Types(IntEnum):
    basic_item = auto()
    basic_equippable = auto()
    weapon = auto()
    armor = auto()


class item:
    def __init__(self, name, dscrpt, val):
        self.item_dict = {'type': Item_Types.basic_item}
        self.item_dict['name'] = name
        self.item_dict['description'] = dscrpt
        self.item_dict['value'] = val

    @property
    def type(self):
        return self.item_dict['type']

    @property
    def value(self):
        return self.item_dict['value']

    @property
    def name(self):
        return self.item_dict['name']

    @property
    def dscrpt(self):
        return self.item_dict['description']


class equippable(item):
    def __init__(self, name, dscrpt, val, hp=0, stren=0, armr=0, agil=0, pwr=0):
        super().__init__(name, dscrpt, val)
        self.item_dict['type'] = Item_Types.basic_equippable
        self.item_dict['stat_change'] = [hp, stren, armr, agil, pwr]

    @property
    def stat_changes(self):
        return self.item_dict['stat_change']


class weapon(equippable):
    def __init__(self, name, dscrpt, val, dmg, linked_attacks, hp=0, stren=0, armr=0, agil=0, pwr=0):
        super().__init__(name, dscrpt, val, hp, stren, armr, agil, pwr)
        self.item_dict['type'] = Item_Types.weapon
        self.item_dict['linked_attack_list'] = linked_attacks

    @property
    def linked_attacks(self):
        return self.item_dict['linked_attack_list']


class armor(equippable):
    def __init__(self, name, dscrpt, val, hp=0, stren=0, armr=0, agil=0, pwr=0):
        super().__init__(name, dscrpt, val, hp, stren, armr, agil, pwr)
        self.item_dict['type'] = Item_Types.armor


class heal_item(item):
    def __init__(self, name, dscrpt, val, hp=0):
        super().__init__(name, dscrpt, val)
        self.item_dict['heal_amount'] = hp

    @property
    def heal_amnt(self):
        return self.item_dict['heal_amount']


class stat_item(equippable):
    def __init__(self, name, dscrpt, val, effect_time, hp=0, stren=0, armr=0, agil=0, pwr=0):
        super().__init__(name, dscrpt, val, hp, stren, armr, agil, pwr)
        self.item_dict['type'] = Item_Types.basic_item
        self.item_dict['effect_time'] = effect_time

    @property
    def duration(self):
        return self.item_dict['effect_time']


#
# Entity Stats #
#

class Stat_Sheet(IntEnum):
    health = 0
    strength = 1
    armor = 2
    agility = 3
    power = 4


class battler_stats:
    def __init__(self, hp, stren, armr, agil, pwr):
        self.stat_dict = {'hp': hp}
        self.stat_dict['max_hp'] = hp
        self.stat_dict['strength'] = stren
        self.stat_dict['armor'] = armr
        self.stat_dict['agility'] = agil
        self.stat_dict['power'] = pwr

    @property
    def health(self):
        return self.stat_dict['hp']

    @health.setter
    def health(self, value):
        self.stat_dict['hp'] = value

    @property
    def max_health(self):
        return self.stat_dict['max_hp']

    @max_health.setter
    def max_health(self, value):
        self.stat_dict['max_hp'] = value

    @property
    def stren(self):
        return self.stat_dict['strength']

    @stren.setter
    def stren(self, value):
        self.stat_dict['strength'] = value

    @property
    def armor(self):
        return self.stat_dict['armor']

    @armor.setter
    def armor(self, value):
        self.stat_dict['armor'] = value

    @property
    def agility(self):
        return self.stat_dict['agility']

    @agility.setter
    def agility(self, value):
        self.stat_dict['agility'] = value

    @property
    def power(self):
        return self.stat_dict['power']

    @power.setter
    def power(self, value):
        self.stat_dict['power'] = value

    @property
    def stat_list(self):
        return [self.health, self.max_health, self.stren, self.armor, self.agility, self.power]

    @stat_list.setter
    def stat_list(self, val):
        try:
            self.health += val[Stat_Sheet.health]
            self.max_health += val[Stat_Sheet.health]
            self.stren += val[Stat_Sheet.strength]
            self.armor += val[Stat_Sheet.armor]
            self.agility += val[Stat_Sheet.agility]
            self.power += val[Stat_Sheet.power]
        except IndexError as e:
            debug_info(e, 'battler_stats.stat_list only accepts lists as setters.', True)
        except TypeError as e:
            debug_info(e, 'An item in stat_change was not a number.', True)

    def writeout(self):
        print(f"Health: {self.health}/{self.max_health}")
        print(f"Strength: {self.stren}")
        print(f"Armor: {self.armor}")
        print(f"Agility: {self.agility}")
        print(f"Power: {self.power}", end="\n\n")


#
# Locations #
#


class Directions(IntEnum):
    Up_Left = 11
    Up = 12
    Up_Right = 13
    Left = 21
    Right = 23
    Down_Left = 31
    Down = 32
    Down_Right = 33


class Location_Errors(IntEnum):
    no_exist = 0
    invalid_direction = 1


class Tiles(IntEnum):
    Player = auto()
    Grass = auto()
    Wall = auto()
    Mountain = auto()
    Cave = auto()
    Water = auto()
    Building = auto()
    Lava = auto()
    Dirt = auto()
    Ice = auto()
    Pit = auto()


class location_manager:
    def __init__(self):
        self.xy_dict = {'Errors': []}
        self.xy_dict['Errors'].append("That place doesn't exist.")
        self.xy_dict['Errors'].append("You're carrying too much.")
        self.xy_dict['Errors'].append("You cannot go that way.")
        self.xy_dict['auto_load'] = True
        self.xy_dict['current_map'] = None

    @property
    def auto_load_map(self):
        return self.xy_dict['auto_load']

    @auto_load_map.setter
    def auto_load_map(self, value):
        # Allows user to turn off map loading for certain sections of the game
        if value is True or value is False:
            self.xy_dict['auto_load'] = value
        else:
            raise TypeError('Value must be True or False.')

    @property
    def player_pos(self):
        return self.xy_dict['player_location']

    @player_pos.setter
    def player_pos(self, val):
        self.xy_dict['player_location'] = val

    def load_if_player(self, thing):
        if self.auto_load_map is True:
            pub_chk_pos.send(sender=self)
            if isinstance(thing, player):
                self.load_map(self.player_pos[Locate_Entity.mapid])
        else:
            clr_console()

    def move(self, thing, direction):
        # Insert data collection from map
        if self.chk_boundary(thing.location[Locate_Entity.mapid], direction.value, thing.location[Locate_Entity.coordinates], False) is not False:
            thing.set_loc(self.chk_boundary(thing.location[Locate_Entity.mapid], direction.value, thing.location[Locate_Entity.coordinates], True if isinstance(thing, player) else False, True))
            # Check to see if the map needs to be reloaded
            self.load_if_player(thing)

    def teleport(self, thing, mapid, x, y):
        # Wrap around try just in case the map is mispelled or does not yet exist
        try:
            # Insert data collection from map, and writeout extra details if the entity is a player
            if mapid.send_data((y, x), True if isinstance(thing, player) else False) is True:
                thing.set_loc([y, x], mapid)
                self.load_if_player(thing)

        except NameError as e:
            debug_info(e, 'That map does not exist', True)

    def chk_boundary(self, mapid, direction, start_loc, is_player, print_errors=False):
        # Update coordinates for direction
        if direction is Directions.Up.value:
            new_loc = [start_loc[Locate_Entity.y_cord] - 1, start_loc[Locate_Entity.x_cord]]
        elif direction is Directions.Down.value:
            new_loc = [start_loc[Locate_Entity.y_cord] + 1, start_loc[Locate_Entity.x_cord]]
        elif direction is Directions.Left.value:
            new_loc = [start_loc[Locate_Entity.y_cord], start_loc[Locate_Entity.x_cord] - 1]
        elif direction is Directions.Right.value:
            new_loc = [start_loc[Locate_Entity.y_cord], start_loc[Locate_Entity.x_cord] + 1]

        try:
            # Test if new coordinate is out of bounds
            mapid.layout[new_loc[Locate_Entity.y_cord], new_loc[Locate_Entity.x_cord]]

            # Check if new coordinate is negative
            for i in new_loc:
                if i < 0:
                    if print_errors is True:
                        print(self.xy_dict['Errors'][Location_Errors.invalid_direction])

                    return start_loc

            # Check against the mapid's send_data method to see what it wants the location manager to do
            if mapid.send_data(tuple(new_loc), True if is_player is True else False) is True:
                return new_loc
            else:
                return False

        except IndexError:
            if print_errors is True:
                # Tell the user that it cannot move that way
                print(self.xy_dict['Errors'][Location_Errors.invalid_direction])

            return start_loc

    def detect_tile(self, til, player_til=False):
            from colorama import Fore, Back, Style
            value = ''

            # Set the background color to magenta to signify that the player is there
            if player_til is True:
                value += Back.MAGENTA

            # Set unicode value of character based on Enum value
            if til == Tiles.Grass.value:
                value += Fore.GREEN + Style.BRIGHT + '\u26B6' + Style.RESET_ALL
            elif til == Tiles.Wall.value:
                value += Fore.WHITE + Style.DIM + '\u26DD' + Style.RESET_ALL
            elif til == Tiles.Mountain.value:
                value += Fore.YELLOW + '\u1A12' + Style.RESET_ALL
            elif til == Tiles.Cave.value:
                value += Fore.YELLOW + '\u1A0A' + Style.RESET_ALL
            elif til == Tiles.Water.value:
                value += Fore.CYAN + '\u2307' + Style.RESET_ALL
            elif til == Tiles.Building.value:
                value += Fore.WHITE + '\u16A5' + Style.RESET_ALL
            elif til == Tiles.Lava.value:
                value += Fore.RED + Style.BRIGHT + '\u26C6' + Style.RESET_ALL
            elif til == Tiles.Dirt.value:
                value += Fore.YELLOW + Style.BRIGHT + '\u26C6' + Style.RESET_ALL
            elif til == Tiles.Ice.value:
                value += Fore.CYAN + Style.BRIGHT + '\u26C6' + Style.RESET_ALL
            elif til == Tiles.Pit.value:
                value += Fore.BLACK + Style.DIM + '\u25CF' + Style.RESET_ALL

            return value

    def load_map(self, mapid, rows=None, clmns=None):
        clr_console()

        # Get player position through event
        pub_chk_pos.send(sender=self)

        # Auto generate columns and rows if they are not provided
        if clmns is None:
            clmns = mapid.layout.shape[Locate_Entity.x_cord]
        if rows is None:
            rows = mapid.layout.shape[Locate_Entity.y_cord]

        # Loop through rows and columns to send each one to the detect_tile method
        for y in range(rows):
            for x in range(clmns):
                # Test for player position against tile
                if ([y, x] == self.player_pos[Locate_Entity.coordinates]) and (mapid is self.player_pos[Locate_Entity.mapid]):
                    print(self.detect_tile(mapid.layout[y, x], True), end=' ')
                else:
                    print(self.detect_tile(mapid.layout[y, x]), end=' ')

            print()

        # Update the current mapid
        self.xy_dict['current_map'] = mapid


class array_map(ABC):
    def __init__(self, name):
        self.map_dict = {'map_id': name}
        self.map_dict['map_layout'] = None

    @abstractmethod
    def send_data(self, til, plyr=False):
        raise NotImplementedError('Please define this method.')
        # TEMPLATE #
        #
        # import os
        # os.system('cls' if os.name == 'nt' else 'clear')
        #
        # if til == [0, 1]:
        #     if plyr is True:
        #         print('You walk forward, and see a massive tree. You step closer.')
        #     return True
        # elif til == [0, 2]:
        #     if player is True:
        #         print('A wide river halts your progress down this path.')
        #     return False

    def chk_tile_val(self, tile, to_match):
            if self.layout[tile[Locate_Entity.y_cord], tile[Locate_Entity.x_cord]] == to_match:
                return True
            else:
                return False

    @property
    def id(self):
        return self.map_dict['map_id']

    @property
    def layout(self):
        return self.map_dict['map_layout']

    @layout.setter
    def layout(self, value):
        assert isinstance(value, np.ndarray)
        self.map_dict['map_layout'] = value

#
# Battle Backend #
#


class attack:
    def __init__(self, name, dscrpt, dmg, acc=100, count=Enumerators.times_attacking, debuff=None):
        self.attack_dict = {'dmg': dmg}
        self.attack_dict['name'] = name
        self.attack_dict['description'] = dscrpt
        self.attack_dict['accuracy'] = acc
        self.attack_dict['hit_count'] = count
        self.attack_dict['debuff_effect'] = debuff

    @property
    def name(self):
        return self.attack_dict['name']

    @property
    def hit_rate(self):
        return self.attack_dict['accuracy']

    @property
    def debuff(self):
        return self.attack_dict['debuff_effect']

    @property
    def dmg(self):
        return self.attack_dict['dmg']

    @property
    def dscrpt(self):
        return self.attack_dict['description']

    @property
    def count(self):
        return self.attack_dict['hit_count']


class ammo_attack(attack):
    def __init__(self, name, dscrpt, dmg, ammo_type, ammo_cost, acc=100, count=Enumerators.times_attacking, debuff=None):
        super().__init__(name, dscrpt, dmg, acc, count, debuff)
        self.attack_dict['accuracy'] = acc
        self.attack_dict['ammo_type'] = ammo_type
        self.attack_dict['ammo_cost'] = ammo_cost

    @property
    def ammo_type(self):
        return self.attack_dict['ammo_type']

    @property
    def ammo_cost(self):
        return self.attack_dict['ammo_cost']

#
# Inventory #
#


class item_collection(ABC):
    def __init__(self, coin, items=list()):
        self.collect_dict = {'collection': items}
        self.collect_dict['currency'] = coin
        self.collect_dict['Error_No_Exist'] = "That item doesn't exist in this inventory."

    def add_item(self, itm, amnt=Enumerators.items_to_modify):
        for i in range(amnt):
            self.items.append(itm)

    def rem_item(self, itm, amnt=Enumerators.items_to_modify):
        for i in range(amnt):
            try:
                self.items.remove(itm)
                return True
            except ValueError:
                print(f"There is/are no more {itm.name} to use, sell, or buy.")
                return False

    @property
    def items(self):
        return self.collect_dict['collection']

    @property
    def coin(self):
        return self.collect_dict['currency']

    @coin.setter
    def coin(self, value):
        if self.coin != Enumerators.infinite_coin:
            self.collect_dict['currency'] += value


class vendor_collection(item_collection):
    def __init__(self, coin, items=list()):
        super().__init__(coin, items)

    def swap_item(self, swapee, itm, count=Enumerators.items_to_modify):
        if itm in self.items:
            for i in range(count):
                if (swapee.collection.coin >= (itm.value * count)) or swapee.collection.coin == Enumerators.infinite_coin:
                    # Swap items
                    swapee.collection.add_item(itm)
                    self.rem_item(itm)
                    # Swap coin
                    swapee.collection.coin = (itm.value * -1)
                    self.coin = itm.value
                else:
                    print(f"{swapee.name} ran out of money.")
        else:
            self.collect_dict['Error_No_Exist']


class battler_collection(item_collection):
    def __init__(self, coin, items, equipped):
        super().__init__(coin, items)
        self.collect_dict['on_entity'] = equipped
        self.collect_dict['Errors'] = "Couldn't equip item."

        if len(self.equipped) > 0:
            self.update_stats()

    @property
    def equipped(self):
        return self.collect_dict['on_entity']

    @property
    def item_stats(self):
        temp = [0, 0, 0, 0, 0]
        for i in range(len(self.equipped)):
            temp = [temp[j] + self.equipped[i].stat_changes[j] for j in range(len(temp))]

        return temp

    def update_stats(self):
        pub_stat_change.send(sender=self, changes=self.item_stats)

    def equip(self, itm):
        try:
            if itm in self.items:
                for i in range(len(self.equipped)):
                    if itm.__class__ == self.equipped[i].__class__:
                        del self.equipped[i]

                self.equipped.append(itm)
                self.update_stats()
            else:
                print(self.collect_dict['Error_No_Exist'])

        except AttributeError:
            print(self.collect_dict['Errors'])

    def move_item(self, itm, movee):
        if self.rem_item(itm) is True:
            movee.collection.add_item(itm)


class player_collection(battler_collection, vendor_collection):
    def __init__(self, coin, items, equipped):
        super().__init__(coin, items, equipped)

    def add_item(self, itm, amnt=Enumerators.items_to_modify):
        for i in range(amnt):
            self.items.append(itm)

        pub_item_obtained.send(sender=self, itms=self.items)

#
# Quests #
#


# In progress
class quest(ABC):
    def __init__(self, name):
        self.quest_dict['name'] = name
        self.quest_dict['current_stage'] = None
        # Not sure if this part of the dictionary is necessary
        # self.quest_dict['stages'] = []

    @property
    def stage(self, stage):
        return self.quest_dict['current_stage']

    @stage.setter
    @abstractmethod
    def stage(self, stage):
        raise NotImplementedError('Please define this method.')
        """
        Here the user will implement anything they require in order to get their quest to function as desired.

        Some possibilities include checking for items in the iventory: subscribe to the pub_item_obtained event and check the player's inventory for items. Check if a player has stepped
        onto a tile by writing a quest.stage method into the array_map class's send_data method. Or, make NPCs say certain things by creating an if statement to check if a quest has a certain stage.
        """


#
# Battle System #
#

class Turn(IntEnum):
    Attack = 0
    Defend = 1


class Enemy_Choices(IntEnum):
    Attack = 0
    Item = 1


class TurnComplete(Exception):
    pass


class battle_manager:
    def __init__(self):
        self.e = 2.7182
        self.battle_dict = {'turn': 0, 'total_turns': 0}

        self.battle_dict['effect_dict'] = {'active_effect_enemy': False}
        self.battle_dict['effect_dict']['active_effect_player'] = False

        self.battle_dict['effect_dict']['reverse_effect_enemy'] = []
        self.battle_dict['effect_dict']['reverse_effect_player'] = []

        self.battle_dict['ai'] = {'used_item': 7}

    def randnum(self, hi, lo=1):
        from random import randint
        return randint(lo, hi)

    def calc_agility(self, agi):
        return round((150) / (1 + (self.e ** ((-1 / 30) * agi))) - 75)

    def determine_first_turn(self, plyr, enemy):
        if plyr.stats.power > enemy.stats.power:
            self.battle_dict['turn'] = Turn.Attack
        elif plyr.stats.power < enemy.stats.power:
            self.battle_dict['turn'] = Turn.Defend
        elif plyr.stats.power == enemy.stats.power:
            if plyr.stats.agility < enemy.stats.agility:
                self.battle_dict['turn'] = Turn.Defend
            else:
                self.battle_dict['turn'] = Turn.Attack

    def clean_active_effect(self):
        temp = self.battle_dict['effect_dict']['reverse_effect_player']

        for i in range(len(self.battle_dict['effect_dict']['reverse_effect_player'])):
            if temp[i][0] > self.battle_dict['total_turns']:
                del temp[i]

        self.battle_dict['effect_dict']['reverse_effect_player'] = temp

        temp = self.battle_dict['effect_dict']['reverse_effect_player']

        for i in self.battle_dict['effect_dict']['reverse_effect_enemy']:
            if temp[i][0] > self.battle_dict['total_turns']:
                del temp[i]

        temp = self.battle_dict['effect_dict']['reverse_effect_enemy']

        del temp

    def refresh_active_effect(self, plyr, enemy):
        if (self.battle_dict['effect_dict']['active_effect_player'] is True) or (self.battle_dict['effect_dict']['active_effect_enemy'] is True):
            if self.battle_dict['effect_dict']['active_effect_player'] is True:
                for i in self.battle_dict['effect_dict']['reverse_effect_player']:
                    if self.battle_dict['turn'] == i[0]:
                        self.use_item_stat(plyr, i[1])

                if self.battle_dict['effect_dict']['reverse_effect_player'] == []:
                    self.battle_dict['effect_dict']['active_effect_player'] = False

            if self.battle_dict['effect_dict']['active_effect_enemy'] is True:
                for i in self.battle_dict['effect_dict']['reverse_effect_enemy']:
                    if self.battle_dict['turn'] == i[0]:
                        self.use_item_stat(plyr, i[1])
                if self.battle_dict['effect_dict']['reverse_effect_enemy'] == []:
                    self.battle_dict['effect_dict']['active_effect_enemy'] = False

            self.clean_active_effect()

    def reverse_item_stat(self, stat_list):
        def invert(val):
            return val * -1

        return [invert(i) for i in stat_list]

    def calc_effect_queue(self, thing, itm):
        try:
            if itm.duration > 0:
                if isinstance(thing, player):
                    self.battle_dict['effect_dict']['active_effect_player'] = True
                    self.battle_dict['effect_dict']['reverse_effect_player'].append((self.battle_dict['turn'] + itm.duration, self.reverse_item_stat(itm.stat_changes)))
                    self.battle_dict['effect_dict']['reverse_effect_player'].sort()
                else:
                    self.battle_dict['effect_dict']['active_effect_enemy'] = True
                    self.battle_dict['effect_dict']['reverse_effect_enemy'].append((self.battle_dict['turn'] + itm.duration, self.reverse_item_stat(itm.stat_changes)))
                    self.battle_dict['effect_dict']['reverse_effect_enemy'].sort()

        except AttributeError as e:
            debug_info(e, 'An incorrect object type was used as type stat_item in battle_manager.use_item().')

    def use_item_stat(self, thing, stat_changes):
        thing.stats.stat_list = stat_changes

    def use_attack(self, user, target, attk):
        # Check if attack hits
        if (self.randnum(100) <= attk.hit_rate) and (self.randnum(100) >= self.calc_agility(target.stats.agility)):
                # Attack landed; calculate damage
                temp_damage = round(((user.stats.stren * attk.dmg ** (user.stats.stren ** .05)) ** .5) + self.randnum(round((user.stats.stren / 2) ** (1/2))))
                temp_damage_recieved = round(temp_damage - target.stats.armor ** (4 / 5))

                if temp_damage_recieved < 1:
                    temp_damage_recieved = 1
                # Check for crit and write out result
                if self.randnum(100) <= self.calc_agility(user.stats.agility):
                    # Indicate critical hit
                    temp_damage_recieved *= 3/2
                    temp_damage_recieved = round(temp_damage_recieved)
                    write((f"{user.name} used {attk.name}.", "It was a critical hit!", f"{user.name} dealt {temp_damage_recieved} to {target.name}."))
                else:
                    # No crit
                    write(f"{user.name} used {attk.name}, and dealt {temp_damage_recieved} damage to {target.name}.")

                target.stats.health -= temp_damage_recieved

                del temp_damage
                del temp_damage_recieved
                self.hit_animate()
                try:

                    # Check for debuffs and apply them
                    self.attack_use_debuff(target, attk.debuff)
                except (AttributeError, TypeError):
                    pass

                try:
                    user.collection.rem_item(attk.ammo_type, attk.ammo_cost)
                except AttributeError:
                    pass

                return False

        else:
            # Attack missed, end turn
            write(f"{user.name} tried to use {attk.name}, but they missed.")
            return False

    def attack_use_debuff(self, target, debuff):
        if isinstance(debuff, stat_item):
            self.calc_effect_queue(target, debuff)
            self.use_item_stat(target, debuff.stat_changes)

    def use_item(self, thing, itm):
        # if itm.stat_changes != [0, 0, 0, 0, 0]:
        # Add above check to the item list generator
        if itm in thing.collection.items:
            try:
                # Add specific instructions for healing items
                if isinstance(itm, heal_item):
                    if thing.stats.health + itm.heal_amnt > thing.stats.max_health:
                        thing.stats.health = thing.stats.max_health
                    else:
                        thing.stats.health += itm.heal_amnt
                elif isinstance(itm, stat_item):
                    self.calc_effect_queue(thing, itm)
                    self.use_item_stat(thing, itm.stat_changes)

                thing.collection.rem_item(itm)

            except ValueError:
                print(f"This item does not exist in {thing.name}'s inventory.")

    def chance_item(self, enemy):
        enemy_has_stat_items = [isinstance(i, stat_item) for i in enemy.collection.items]
        enemy_has_heal_items = [isinstance(i, heal_item) for i in enemy.collection.items]

        if (True in enemy_has_stat_items) and (self.battle_dict['ai']['used_item'] > 0):
            return round((100) / (1 + (self.e ** ((-1 / 2) * self.battle_dict['ai']['used_item']))) - 50)
        elif (True in enemy_has_heal_items) and (self.battle_dict['ai']['used_item'] > 0):
            return self.chance_heal(enemy)
        else:
            return 0

    def chance_heal(self, enemy):
        enemy_has_heal_items = [isinstance(i, heal_item) for i in enemy.collection.items]

        def percent_health():
            return 100 - (((enemy.stats.max_health - enemy.stats.health) / enemy.stats.max_health) * 100)

        if (True in enemy_has_heal_items) and (percent_health() <= 80):
            return round(-25719423 + (89.67716 - -25719430)/(1 + ((percent_health() / 1720762) ** 1.286616)))
        else:
            return 0

    def switch_turn(self, power_data, enemy_used_item=False):
        if power_data[0] < power_data[1]:
            power_data[0] += 1
        else:
            if self.battle_dict['turn'] == Turn.Attack:
                # Switch turn
                self.battle_dict['turn'] = Turn.Defend
                # Exit turn
                raise TurnComplete
            elif self.battle_dict['turn'] == Turn.Defend:
                # Switch turn
                self.battle_dict['turn'] = Turn.Attack
                # Do extras based on item use
                if enemy_used_item is True:
                    self.battle_dict['ai']['used_item'] = 0
                else:
                    self.battle_dict['ai']['used_item'] += 1
                # Exit turn
                raise TurnComplete
            else:
                debug_info(ValueError('The turn counter was not set correctly.'), 'Somehow, the value of turn was switched away from 0 or 1, which are the accepted values.')

    def hit_animate(self):
        pass

    def draw_hp(self, plyr, enemy):
        prcnt_plyr_health = round((plyr.stats.health / plyr.stats.max_health) * 100)

        print('[', end='')
        for i in range(100):
            print('=' if i <= prcnt_plyr_health else '-', end='')
        print(']')

        del prcnt_plyr_health

        prcnt_enemy_health = round((enemy.stats.health / enemy.stats.max_health) * 100)
        print('[', end='')
        for i in range(100):
            print('=' if i <= prcnt_enemy_health else '-', end='')
        print(']')

        del prcnt_enemy_health

    def enemy_use_heal_item(self, enemy):
        # Use healing item

        temp_heal_items = []
        for heal in enemy.collection.items:
            if isinstance(heal, heal_item):
                temp_heal_items.append(heal)

        heals_ordered_best = []

        # Generate list of healing items that don't overheal the enemy
        for heal in temp_heal_items:
            if enemy.stats.health + heal.heal_amnt <= enemy.stats.max_health:
                heals_ordered_best.append((heal.heal_amnt, heal))

        del temp_heal_items

        if heals_ordered_best != []:
            # Order them by what item will heal them the most
            heals_ordered_best.sort(reverse=True)

            # Use the item
            write(f"{enemy.name} used a {heals_ordered_best[0][1].name}, and regained {heals_ordered_best[0][1].heal_amnt} health.")
            self.use_item(enemy, heals_ordered_best[0][1])

            # Delete unneeded var
            del heals_ordered_best
            return True


        # Create list of healing items and sort them based on how effective they are
        temp_heal_list = []
        for heal in enemy.collection.items:
            if isinstance(heal, heal_item):
                temp_heal_list.append((heal.heal_amnt, heal))
        temp_heal_list.sort()

        # Use item and display its use
        write(f"{enemy.name} used a {temp_heal_list[0][1].name} and regained {enemy.stats.max_health - enemy.stats.health} health.")
        self.use_item(enemy, temp_heal_list[0][0])

        # Finish up
        del temp_heal_list
        del heals_ordered_best
        return True

    def enemy_use_item(self, enemy):
        # Use item #
        # Generate random number
        enemy_choice = self.randnum(100)
        # Check if there are valid items or not
        valid_stat_items = (isinstance(itm, stat_item) for itm in enemy.collection.items)
        if (enemy_choice <= self.chance_heal(enemy)) or all(check is False for check in valid_stat_items):
            self.enemy_use_heal_item(enemy)
        else:
            # Use buff item

            # Generate list of places in inventory where buff items exist
            temp_stat_items = []
            for i in range(len(enemy.collection.items)):
                if isinstance(enemy.collection.items[i], stat_item):
                    temp_stat_items.append(i)

            # Randomly select buff from list of places in inventory
            enemy_choice = self.randnum(len(temp_stat_items) - 1, 0)
            buff_choice = enemy.collection.items[temp_stat_items[enemy_choice]]

            # Tell player and use buff
            write(f"{enemy.name} used a {buff_choice.name}.")
            self.use_item(enemy, buff_choice)

            del temp_stat_items
            return True

    def enemy_determine_attack(self, enemy):
        while True:
            random_attack = enemy.attacks[self.randnum(len(enemy.attacks)) - 1]

            if isinstance(random_attack, ammo_attack):
                req_items = 0
                for itm in enemy.collection.items:
                    if itm is random_attack.ammo_type:
                        req_items += 1

                if req_items >= random_attack.ammo_cost:
                    return random_attack

            elif isinstance(random_attack, ammo_attack) is False:
                return random_attack

    def battle(self, plyr, enemy, spec_effect=None):
        self.determine_first_turn(plyr, enemy)

        while (plyr.stats.health > 0) and (enemy.stats.health > 0):
            # Allow player to read before clearing screen
            clr_console()
            self.draw_hp(plyr, enemy)

            # Check to make sure no effects are active that shouldn't be
            self.refresh_active_effect(plyr, enemy)

            # Run the spec_effect if there is one specified
            if spec_effect is not None:
                spec_effect()

            # Increase turn counter
            self.battle_dict['total_turns'] += 1

            # Check if player is attacking or defending
            try:
                temp_power = 1
                # Determine whose turn it is
                if self.battle_dict['turn'] == Turn.Attack:
                    # Loop for power
                    while True:
                        pass

                if self.battle_dict['turn'] == Turn.Defend:
                    while True:
                        enemy_choice = self.randnum(100)
                        # Test if enemy uses item
                        if enemy_choice <= self.chance_item(enemy):
                            self.switch_turn([temp_power, enemy.stats.power], self.enemy_use_item(enemy))
                        else:
                            # Attack
                            self.switch_turn([temp_power, enemy.stats.power], self.use_attack(enemy, plyr, self.enemy_determine_attack(enemy)))

            except TurnComplete:
                input('\nPress enter to continue.')
                pass

        if plyr.stats.health > 0:
            pass
        else:
            pass


#
# Tracker #
#

class object_tracker:
    def __init__(self):
        self.one_time_init = 0

    def empty_tracker(self):
        if self.one_time_init != 0:
            self.track_dict.update((key, []) for key in self.track_dict)
        else:
            self.track_dict = {}
            self.one_time_init = 1

    def categ_list(self, globl):
        # check for Gilbo-defined class parents
        try:
            import inspect
            if 'Gilbo' in str(inspect.getfile(globl.__class__)).split('\\')[-1]:
                temp = []
                parents = inspect.getmro(globl.__class__)

                # Append list of matched objects to temporary list
                for i in range(len(parents)):
                    temp_append = str(parents[i]).split("'")[1]
                    try:
                        temp_append = temp_append.split('.')[1]
                    except IndexError:
                        pass
                    temp.append(temp_append)

                # Append globals that match the object to list
                for i in range(len(temp)):
                    try:
                        self.track_dict[temp[i]].append(globl)
                    except KeyError:
                        self.track_dict.update({temp[i]: [globl]})

                del temp

        except TypeError:
            pass

    def update_tracker(self, class_list, spec_search=None):
        self.empty_tracker()

        # Check if user wants to search for a specific item
        if spec_search is None:
            for key in class_list:
                if isinstance(class_list[key], list):
                    for i in range(len(class_list[key])):
                        self.categ_list(class_list[key][i])
                else:
                    self.categ_list(class_list[key])

        else:
            # If the user wants to search for something specifically, begin another process
            store_names = []
            import inspect

            for key in class_list:
                try:
                    if 'Gilbo' in str(inspect.getfile(class_list[key].__class__)).split('\\')[-1]:
                        # Find instances of the searched term
                        if isinstance(class_list[key], spec_search):
                            store_names.append(class_list[key])

                except TypeError:
                    pass

            return store_names

    def read_write_data(self, data_set=[]):
        for i in range(len(data_set)):
            print(data_set[i])

        print('\n')

    def writeout(self, spec_search=None):
        print()
        for i, j in self.tracker.items():
            if spec_search is None:
                self.read_write_data([i, j])
            elif spec_search is not None and str(i) == spec_search:
                self.read_write_data([i, j])

    def save_data(self, obj_list):
        keys = list(obj_list.keys())
        values = list(obj_list.values())

        with open('sav.pickle', 'wb') as handle:
            handle.truncate(0)
            import dill as pickle
            pickle.dump((keys, values), handle)

        del keys, values

    def load_data(self, obj_list):
        with open('sav.pickle', 'rb') as handle:
            import dill as pickle
            keys, values = pickle.load(handle)
            for i in range(len(keys)):
                try:
                    obj_list.update({keys[i]: values[i]})
                except IndexError as e:
                    debug_info(e, 'There was more data to load than exists now', True)

    @property
    def tracker(self):
        return self.track_dict


tracker = object_tracker()
loc_man = location_manager()
bat_man = battle_manager()
