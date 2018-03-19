from abc import ABC, abstractmethod
from random import randint
from time import sleep
from enum import Enum, IntFlag

# 3rd Party Libraries
import numpy as np
from blinker import signal
from colorama import Fore, Back, Style

# Links to remember
# ascii-table.com/ansi-escape-sequences.php
# https://unicode-table.com/en/blocks/box-drawing/


#
# Events #
#

# Inventory-related
item_obtained = signal('check-carry-weight')
item_equipped = signal('update-properties')

# Entity-position-related
chk_plyr_pos = signal('check-position')

#
# Common Enumerators #
#


class Enumerators(IntFlag):
    # Stat enums
    base_carry_cap = 100
    carry_cap_modifier = 2
    # Inventory enums
    items_to_modify = 1
    # Attack enums
    base_ammo_cost = 1
    times_attacking = 1


#
# Functions #
#


def type(phrase, type_speed=.045, line_delay=.5):
    for i in range(len(phrase)):
        print(phrase[i], end="", flush=True)
        sleep(type_speed)

    sleep(line_delay)


#
# Abstract class from which all enemies, NPCs, and players are derived. #
#


class Locate_Entity(Enum):
    map_name = 0
    coordinates = 1
    x_coordinate = 2
    y_coordinate = 3


class entity(ABC):
    def __init__(self, name, location, x, y):
        self.entity_dict = {}
        self.entity_dict['name'] = name
        self.entity_dict['location'][Locate_Entity.map_name] = location.id
        self.entity_dict['location'][Locate_Entity.coordinates] = [x, y]
        self.entity_dict['location'][Locate_Entity.x_coordinate] = x
        self.entity_dict['location'][Locate_Entity.y_coordinate] = y

    @property
    def name(self):
        return self.entity_dict['name']

    @name.setter
    def name(self, value):
        self.entity_dict['name'] = value

    @property
    def location(self):
        return self.entity_dict['location']

    def set_loc(self, location, x, y):
        self.entity_dict['location'][Locate_Entity.map_name] = location.id
        self.entity_dict['location'][Locate_Entity.index_num] = location.layout[x, y]



class NPC(entity):
    def __init__(self, name, location, x, y):
        super().__init__(name, location, x, y)
        self.dialogue_dict = {}

    def add_dialogue(self, diag_name, diag_content):
        self.dialogue_dict[diag_name] = diag_content

    def type_dialogue(self, diag_name):
        for i in range(len(self.dialogue_dict[diag_name])):
            type(self.dialogue_dict[diag_name][i])


class vendor(entity):
    def __init__(self, name, location, x, y, inv, coin):
        super().__init__(name, location, x, y)
        self.entity_dict['inventory'] = inv
        self.entity_dict['currency'] = coin

    @property
    def coin(self):
        return self.entity_dict['currency']

    @coin.setter
    def coin(self, value):
        self.entity_dict['currency'] += value

    @property
    def inv(self):
        return self.entity_dict['inventory']


class battler(vendor):
    def __init__(self, name, location, x, y, inv, coin, stats):
        super().__init__(name, location, x, y, inv, coin)
        self.entity_dict['stats'] = stats
        self.Error_Incorrect_Inventory = 'Incorrect inventory class.'

    @property
    def stats(self):
        return self.entity_dict['stats']

    @property
    def attacks(self):
        try:
            for i in range(len(self.inv.equipped)):
                if isinstance(self.inv.equipped[i], weapon):
                    return self.inv.equipped[i]
        except AttributeError:
            print(self.Error_Incorrect_Inventory)


class player(battler):
    def __init__(self, name, location, x, y, inv, coin, stats):
        super().__init__(name, location, x, y, inv, coin, stats)

    @chk_plyr_pos.connect
    def get_location(self):
        loc_man.player_pos = self.location

#
# Items/Weapons in the game #
#


class Item_Types(Enum):
    basic_item = 0
    basic_equippable = 1
    weapon = 2
    armor = 3


class item_unweighted:
    def __init__(self, name, dscrpt):
        self.item_dict = {}
        self.item_dict['type'] = Item_Types.basic_item
        self.item_dict['name'] = name
        self.item_dict['description'] = dscrpt

    @property
    def type(self):
        return self.item_dict['type']

    @property
    def name(self):
        return self.item_dict['name']

    @property
    def dscrpt(self):
        return self.item_dict['description']


class item_weighted(item_unweighted):
    def __init__(self, name, dscrpt, weight, val):
        super().__init__(name, dscrpt)
        self.item_dict['type'] = Item_Types.basic_item
        self.item_dict['carry_weight'] = weight
        self.item_dict['value'] = val

    @property
    def weight(self):
        return self.item_dict['carry_weight']

    @property
    def value(self):
        return self.item_dict['value']


class equippable(item_weighted):
    def __init__(self, name, dscrpt, weight, val):
        super().__init__(name, dscrpt, weight, val)
        self.item_dict['type'] = Item_Types.basic_equippable

    # The API users will have to define their own equip effect


class weapon(equippable):
    def __init__(self, name, dscrpt, weight, val, dmg, linked_attacks=list()):
        super().__init__(name, dscrpt, weight, val)
        self.item_dict['type'] = Item_Types.weapon
        self.item_dict['wpn_dmg'] = dmg
        self.item_dict['linked_attack_list'] = linked_attacks

        @property
        def attacks(self):
            return self.item_dict['linked_attack_list']


class armor(equippable):
    def __init__(self, name, dscrpt, weight, val, armr):
        super().__init__(name, dscrpt, weight, val)
        self.item_dict['type'] = Item_Types.armor
        self.item_dict['wpn_dmg'] = armr


class heal_item(item_weighted):
    def __init__(self, name, dscrpt, weight, val, heal_amnt):
        super().__init__(name, dscrpt, weight, val)
        self.item_dict['heal_amount'] = heal_amnt
        self.item_dict['type'] = Item_Types.basic_item

#
# Entity Stats #
#


class battler_stats:
    def __init__(self, hp, stren, armr, agil, pwr):
        self.stat_dict = {}
        self.stat_dict['hp'] = hp
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


class player_stats(battler_stats):
    def __init__(self, hp, stren, armr, agil, pwr):
        super().__init__(hp, stren, armr, agil, pwr)
        self.calc_carry_cap()

    overencumbered = False

    def calc_carry_cap(self):
        self.stat_dict['carry_capacity'] = Enumerators.base_carry_cap + self.stat_dict['strength'] * Enumerators.carry_cap_modifier

    @property
    def over_enc(self):
        return self.overencumbered

    @over_enc.setter
    def over_enc(self, value):
        self.overencumbered = value
        # WRITE MORE HERE FOR WHAT OVERENCUMBENCE AFFECTS

    @property
    def stren(self):
        return self.stat_dict['strength']

    @stren.setter
    def stren(self, value):
        self.stat_dict['strength'] = value
        self.calc_carry_cap()

    @item_obtained.connect
    def check_carry_weight(self, **kw):
        total_weight = None

        for i in range(len(kw['item'])):
            total_weight += kw['item'][i].weight

        if total_weight > self.calc_carry_cap():
            self.over_enc = True

#
# Locations #
#


class Directions(Enum):
    Up_Left = 0
    Up = 1
    Up_Right = 2
    Left = 2
    Right = 3
    Down_Left = 4
    Down = 5
    Down_Right = 6


class Location_Errors(Enum):
    no_exist = 0
    encumbered = 1
    invalid_direction = 2


class Tiles(Enum):
    Player = 0
    Grass = 1
    Wall = 2
    Mountain = 3
    Cave = 4
    Water = 5
    Building = 6
    Lava = 7
    Dirt = 8
    Ice = 9
    Pit = 10


class location_manager:
    def __init__(self):
        self.xy_dict = {}
        self.xy_dict['Error_Message'][Location_Errors.no_exist] = "That place doesn't exist."
        self.xy_dict['Error_Message'][Location_Errors.encumbered] = "You're carrying too much."
        self.xy_dict['Error_Message'][Location_Errors.invalid_direction] = "You cannot go that way."

        tracker.update_tracker()
        self.xy_dict['maps'] = tracker.tracker['maps']
        self.xy_dict['quests'] = tracker.tracker['quests']

    @property
    def player_pos(self, value):
        return self.xy_dict['player_location']

    @player_pos.setter
    def player_pos(self, value):
        self.xy_dict['player_location'] = value

    def reload(self):
        tracker.update_tracker()
        self.xy_dict['maps'] = tracker.tracker['maps']
        self.xy_dict['quests'] = tracker.tracker['quests']

    def move(self, thing, direction):
        if isinstance(thing.inv, player_collection) and entity.inv.over_enc is True:
            return print(self.xy_dict['Error_Message'][Location_Errors.encumbered])
        # Insert data collection from map
        self.check_bounds(thing.location[Locate_Entity.map_name], direction, thing.location[Locate_Entity.x_coordinate], thing.location[Locate_Entity.y_coordinate])

    def teleport(self, thing, mapid, x, y):
        if mapid in self.xy_dict['maps']:
            if isinstance(thing.inv, player_collection) and thing.inv.over_enc is True:
                return print(self.xy_dict['Error_Message'][Location_Errors.encumbered])
            # Insert data collection from map
            return mapid.send_data(list(x, y))
        else:
            return print(self.xy_dict['Error_Message'][Location_Errors.no_exist])

    def check_bounds(self, mapid, direction, x, y):
        if direction is Directions.Up:
            new_place = list(x, y + 1)
        elif direction is Directions.Down:
            new_place = list(x, y - 1)
        elif direction is Directions.Left:
            new_place = list(x - 1, y)
        elif direction is Directions.Right:
            new_place = list(x + 1, y)
        else:
            return print(self.xy_dict['Error_Message'][Location_Errors.invalid_direction])

        try:
            mapid.layout[new_place]

            return mapid.send_data(new_place)
        except IndexError:
            return print(self.xy_dict['Error_Message'][Location_Errors.invalid_direction])

    def detect_tile(self, til):
            self.value = ' '
            chk_plyr_pos.send()

            if til == .layout[self.player_pos[Locate_Entity.y_coordinate], self.player_pos[Locate_Entity.x_coordinate]]:
                self.value.join(Back.MAGENTA)

            if til == Tiles.Grass:
                self.value.join(Fore.GREEN + Style.BRIGHT + '\u26B6' + Style.RESET_ALL)
            elif til == Tiles.Wall:
                self.value.join(Fore.WHITE + Style.DIM + '\u26DD' + Style.RESET_ALL)
            elif til == Tiles.Mountain:
                self.value.join(Fore.YELLOW + '\u1A12' + Style.RESET_ALL)
            elif til == Tiles.Cave:
                self.value.join(Fore.YELLOW + '\u1A0A' + Style.RESET_ALL)
            elif til == Tiles.Water:
                self.value.join(Fore.CYAN + '\u2307' + Style.RESET_ALL)
            elif til == Tiles.Building:
                self.value.join(Fore.WHITE + '\u16A5' + Style.RESET_ALL)
            elif til == Tiles.Lava:
                self.value.join(Fore.RED + Style.BRIGHT + '\u26C6' + Style.RESET_ALL)
            elif til == Tiles.Dirt:
                self.value.join(Fore.YELLOW + Style.BRIGHT + '\u26C6' + Style.RESET_ALL)
            elif til == Tiles.Ice:
                self.value.join(Fore.CYAN + Style.BRIGHT + '\u26C6' + Style.RESET_ALL)
            elif til == Tiles.Pit:
                self.value.join(Fore.BLACK + Style.DIM + '\u25CF' + Style.RESET_ALL)

            return self.value

    def load_loc(self, mapid, clmns, rows=None):
        if rows is None:
            rows = len(mapid.layout)

        try:
            for y in range(rows):
                for x in range(clmns):
                    print(self.detect_tile(mapid.layout[y, x]), end=' ')
                print()
        except IndexError:
            print(self.xy_dict['Error_Message'][Location_Errors.no_exist])


class matrix_map:
    def __init__(self, name, entities=list()):
        self.map_dict = {}
        self.map_dict['map_id'] = name
        self.map_dict['map_layout'] = None
        self.map_dict['entities'] = entities

    @abstractmethod
    def send_data(self, tile):
        raise NotImplementedError('Please define this method.')

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

    @property
    def entities(self):
        return self.map_dict['entities']

#
# Battle Backend #
#


class attack:
    def __init__(self, dmg, dscrpt, count=Enumerators.times_attacking):
        self.attack_dict = {}
        self.attack_dict['dmg'] = dmg
        self.attack_dict['description'] = dscrpt
        self.attack_dict['hit_count'] = count

    @property
    def dmg(self):
        return self.attack_dict['dmg']

    @property
    def dscrpt(self):
        return self.attack_dict['description']

    @property
    def count(self):
        return self.attack_dict['hit_count']


class ranged_attack(attack):
    def __init__(self, dmg, dscrpt, count, acc, ammo_cost):
        super().__init__(dmg, dscrpt, count)
        self.attack_dict['accuracy'] = acc
        self.attack_dict['ammo_cost'] = ammo_cost

    @property
    def ammo_cost(self):
        return self.attack_dict['ammo_cost']

    @property
    def acc(self):
        return self.attack_dict['accuracy']

#
# Inventory #
#


class item_collection(ABC):
    def __init__(self, items=list()):
        self.items = items

    def add_itm(self, itm, amnt=Enumerators.items_to_modify):
        for i in range(amnt):
            self.items.append(itm)

    def rem_itm(self, itm, amnt=Enumerators.items_to_modify):
        for i in range(amnt):
            if itm in self.items:
                self.items.remove(itm)
            else:
                print("There is/are no more " + itm.name + " to use, sell, or buy.")

    @property
    def inventory(self):
        return self.items


class vendor_collection(item_collection):
    def __init__(self, items):
        super().__init__(items)
        self.Error_No_Exist = "That item doesn't exist in this inventory."

    def swap_item(self, item, swapee, count=1):
        if item in self.items:
            for i in range(count):
                if swapee.coin >= (item.value * count):
                    swapee.inv.add_itm(item)
                    self.rem_itm(item)
                    self.coin = item.value
                else:
                    print(swapee.name + " ran out of money.")
        else:
            print(self.Error_No_Exist)


class battler_collection(item_collection):
    def __init__(self, items, equipped=list()):
        super().__init__(items)
        self.on_entity = equipped
        self.Error_Message = "That didn't work."

    def equip(self, item):
        if item in self.items and isinstance(item, equippable):
            for i in range(len(self.equipped)):
                if item.type is self.on_entity[i].type:
                    del self.on_entity[i]

            self.on_entity.append(item)
            item_equipped.send(item=item)
        else:
            print(self.Error_Message)

        @property
        def equipped(self):
            return self.on_entity


class player_collection(vendor_collection, battler_collection):
    def __init__(self, items, equipped):
        super().__init__(items, equipped)

    def add_itm(self, itm, amnt=Enumerators.items_to_modify):
        for i in range(amnt):
            self.items.append(itm)
            item_obtained.send(item=self.inventory())

#
# Quests #
#


class quest:
    def __init__(self, name):
        # Placeholder
        self.name = name
        pass


#
# Battle System #
#

class battle_manager:
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

    def categ_globals(self, globl, ref_added):
        if isinstance(globl, entity):
            self.track_dict['entities'].append(ref_added); return

        elif isinstance(globl, item_unweighted):
            self.track_dict['items'].append(ref_added); return

        elif isinstance(globl, battler_stats):
            self.track_dict['stat_lists'].append(ref_added); return

        elif isinstance(globl, attack):
            self.track_dict['attacks'].append(ref_added); return

        elif isinstance(globl, matrix_map):
            self.track_dict['maps'].append(ref_added); return

        elif isinstance(globl, item_collection):
            self.track_dict['inventories'].append(ref_added); return

        elif isinstance(globl, quest):
            self.track_dict['quests'].append(ref_added); return

    def update_tracker(self):
        self.empty_tracker()

        for key in globals():
            self.categ_globals(globals()[key], globals()[key])

        if self.one_time_init != 1:
            self.one_time_init = 1

    @property
    def tracker(self):
        return self.track_dict

loc_man = location_manager()
tracker = object_tracker()
