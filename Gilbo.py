# Gilbo RPG API -- Version 0.5.7-C #

from abc import ABC, abstractmethod
from random import randint
from time import sleep
from enum import IntEnum, auto

# 3rd Party Libraries
import numpy as np
from blinker import signal
from colorama import Fore, Back, Style

# ascii-table.com/ansi-escape-sequences.php


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


class Enumerators(IntEnum):
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


class Locate_Entity(IntEnum):
    map_name = auto()
    coordinates = auto()
    x_coordinate = auto()
    y_coordinate = auto()


class entity(ABC):
    def __init__(self, name, location, x, y):
        self.entity_dict = {'location': []}
        self.entity_dict['name'] = name
        self.entity_dict['location'].insert(Locate_Entity.map_name, location.id)
        self.entity_dict['location'].insert(Locate_Entity.coordinates, [x, y])
        self.entity_dict['location'].insert(Locate_Entity.x_coordinate, x)
        self.entity_dict['location'].insert(Locate_Entity.y_coordinate, y)

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
    def collection(self):
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
        def handle_chk_plyr_pos(sender, **kwargs):
            self.on_chk_plyr_pos(sender, **kwargs)
        self.handle_chk_plyr_pos = handle_chk_plyr_pos

    def on_chk_plyr_pos(self):
        loc_man.player_pos = self.location

#
# Items/Weapons in the game #
#


class Item_Types(IntEnum):
    basic_item = auto()
    basic_equippable = auto()
    weapon = auto()
    armor = auto()


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
        self.stat_dict['overencumbered'] = False

        def handle_item_obtained(sender, **kwargs):
            self.on_item_obtained(sender, **kwargs)
        self.handle_item_obtained = handle_item_obtained
        item_obtained.connect(handle_item_obtained)

    def calc_carry_cap(self):
        self.stat_dict['carry_capacity'] = Enumerators.base_carry_cap + self.stat_dict['strength'] * Enumerators.carry_cap_modifier

    @property
    def encumbered(self):
        return self.stat_dict['overencumbered']

    @encumbered.setter
    def encumbered(self, value):
        self.stat_dict['overencumbered'] = value
        # WRITE MORE HERE FOR WHAT OVERENCUMBENCE AFFECTS

    @property
    def stren(self):
        return self.stat_dict['strength']

    @stren.setter
    def stren(self, value):
        self.stat_dict['strength'] = value
        self.calc_carry_cap()

    # @item_obtained.connect
    def on_item_obtained(self, sender, **kwargs):
        total_weight = 0

        for i in range(len(kwargs['items'])):
            total_weight += kwargs['items'][i].weight

        self.calc_carry_cap()

        if total_weight > self.stat_dict['carry_capacity']:
            self.encumbered = True

        del total_weight

#
# Locations #
#


class Directions(IntEnum):
    Up_Left = auto()
    Up = auto()
    Up_Right = auto()
    Left = auto()
    Right = auto()
    Down_Left = auto()
    Down = auto()
    Down_Right = auto()


class Location_Errors(IntEnum):
    no_exist = auto()
    encumbered = auto()
    invalid_direction = auto()


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
        self.xy_dict['Errors'].insert(Location_Errors.no_exist.value, "That place doesn't exist.")
        self.xy_dict['Errors'].insert(Location_Errors.encumbered.value, "You're carrying too much.")
        self.xy_dict['Errors'].insert(Location_Errors.invalid_direction.value, "You cannot go that way.")

    @property
    def player_pos(self, value):
        return self.xy_dict['player_location']

    @player_pos.setter
    def player_pos(self, value):
        self.xy_dict['player_location'] = value

    def move(self, thing, direction):
        if isinstance(thing.inv, player_collection) and entity.inv.encumbered is True:
            return print(self.xy_dict['Errors'][Location_Errors.encumbered])
        # Insert data collection from map
        self.check_bounds(thing.location[Locate_Entity.map_name], direction, thing.location[Locate_Entity.x_coordinate], thing.location[Locate_Entity.y_coordinate])

    def teleport(self, thing, mapid, x, y):
        if mapid in tracker.update_tracker('matrix_map'):
            if isinstance(thing.inv, player_collection) and thing.inv.encumbered is True:
                return print(self.xy_dict['Errors'][Location_Errors.encumbered])
            # Insert data collection from map
            return mapid.send_data(list(x, y))
        else:
            return print(self.xy_dict['Errors'][Location_Errors.no_exist])

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
            return print(self.xy_dict['Errors'][Location_Errors.invalid_direction])

        try:
            mapid.layout[new_place]

            return mapid.send_data(new_place)
        except IndexError:
            return print(self.xy_dict['Errors'][Location_Errors.invalid_direction])

    def detect_tile(self, til):
            self.value = ''
            # chk_plyr_pos.send()

            # if til == self.player_pos.layout[self.player_pos[Locate_Entity.y_coordinate], self.player_pos[Locate_Entity.x_coordinate]]:
            #    self.value += Back.MAGENTA

            if til == Tiles.Grass.value:
                self.value += Fore.GREEN + Style.BRIGHT + '\u26B6' + Style.RESET_ALL
            elif til == Tiles.Wall.value:
                self.value += Fore.WHITE + Style.DIM + '\u26DD' + Style.RESET_ALL
            elif til == Tiles.Mountain.value:
                self.value += Fore.YELLOW + '\u1A12' + Style.RESET_ALL
            elif til == Tiles.Cave.value:
                self.value += Fore.YELLOW + '\u1A0A' + Style.RESET_ALL
            elif til == Tiles.Water.value:
                self.value += Fore.CYAN + '\u2307' + Style.RESET_ALL
            elif til == Tiles.Building.value:
                self.value += Fore.WHITE + '\u16A5' + Style.RESET_ALL
            elif til == Tiles.Lava.value:
                self.value += Fore.RED + Style.BRIGHT + '\u26C6' + Style.RESET_ALL
            elif til == Tiles.Dirt.value:
                self.value += Fore.YELLOW + Style.BRIGHT + '\u26C6' + Style.RESET_ALL
            elif til == Tiles.Ice.value:
                self.value += Fore.CYAN + Style.BRIGHT + '\u26C6' + Style.RESET_ALL
            elif til == Tiles.Pit.value:
                self.value += Fore.BLACK + Style.DIM + '\u25CF' + Style.RESET_ALL

            return self.value

    def load_map(self, mapid, clmns, rows=None):
        if rows is None:
            rows = len(mapid.layout)

        try:
            for y in range(rows):
                for x in range(clmns):
                    print(self.detect_tile(mapid.layout[y, x]), end=' ')
                print()
        except IndexError:
            print(self.xy_dict['Errors'][Location_Errors.no_exist])


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

    def add_item(self, itm, amnt=Enumerators.items_to_modify):
        for i in range(amnt):
            self.items.append(itm)

    def rem_item(self, itm, amnt=Enumerators.items_to_modify):
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
                    swapee.inv.add_item(item)
                    self.rem_item(item)
                    self.coin = item.value
                else:
                    print(swapee.name + " ran out of money.")
        else:
            print(self.Error_No_Exist)


class battler_collection(item_collection):
    def __init__(self, items, equipped=list()):
        super().__init__(items)
        self.on_entity = equipped
        self.Errors = "That didn't work."

    def equip(self, item):
        try:
            if item in self.items:
                for i in range(len(self.on_entity)):
                    if item.__class__ == self.on_entity.__class__:
                        del self.on_entity[i]

            self.on_entity.append(item)
            item_equipped.send(item=item)

        except AttributeError:
            print(self.Errors)

        @property
        def equipped(self):
            return self.on_entity


class player_collection(battler_collection, vendor_collection):
    def __init__(self, items, equipped):
        super().__init__(items, equipped)

    def add_item(self, itm, amnt=Enumerators.items_to_modify):
        for i in range(amnt):
            self.items.append(itm)
            item_obtained.send(self.inventory)

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
        else:
            self.track_dict = {}

    def categ_globals(self, globl):
        # check for Gilbo-defined class parents
        try:
            import inspect
            if 'Gilbo' in str(inspect.getfile(globl.__class__)).split('\\')[-1]:
                temp = []
                parents = inspect.getmro(globl.__class__)

                for i in range(len(parents)):
                    temp_append = str(parents[i]).split("'")[1]
                    try:
                        temp_append = temp_append.split('.')[1]
                    except IndexError:
                        pass
                    temp.append(temp_append)

                for i in range(len(temp)):
                    try:
                        self.track_dict[temp[i]].append(globl)
                    except KeyError:
                        self.track_dict.update({temp[i]: [globl]})

                del temp
        # except AttributeError:
        # print('BROKEN ' + str(globl) + '\n')
        except TypeError:
            pass

    def update_tracker(self, class_list, spec_search=None):
        self.empty_tracker()

        if spec_search is None:
            for key in class_list:

                self.categ_globals(class_list[key])

            if self.one_time_init != 1:
                self.one_time_init = 1
        else:
            store_names = {}

            if spec_search not in globals():
                raise NameError('Object Tracker: that class does not exist.')

            for key in globals():
                if self.get_objects(class_list, spec_search) is not None:
                    store_names[str(key)] = self.get_objects(class_list[key], spec_search)

            return store_names

    def get_objects(self, globl, obj_type):
        if isinstance(globl, obj_type):
            return globl
        else:
            return None

    @property
    def tracker(self):
        return self.track_dict


tracker = object_tracker()
loc_man = location_manager()
