from abc import ABC
from random import randint
from time import sleep
from enum import Enum, IntFlag
from blinker import signal
from numpy import matrix


#
# Events
#

item_obtained = signal('check-carry-weight')

#
# Common Enumerators
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
# Functions
#


def type(phrase, type_speed=.045, line_delay=.5):
    for i in range(len(phrase)):
        print(phrase[i], end="", flush=True)
        sleep(type_speed)

    sleep(line_delay)

#
# Abstract class from which all enemies, NPCs, and players are derived.
#


class entity(ABC):

    def __init__(self, name, location, x, y):
        self.entity_dict = {}
        self.entity_dict['name'] = name
        self.entity_dict['location'] = location.layout[x, y]

    @property
    def name(self):
        return self.entity_dict['name']

    @name.setter
    def name(self, value):
        self.entity_dict['name'] = value

    @property
    def location(self):
        return self.entity_dict['location']

    @location.setter
    def location(self, location, x, y):
        self.entity_dict['location'] = location.layout[x, y]


class NPC(entity):
    def __init__(self, name, dialogue):
        super().__init__(name)


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
    def __init__(self, name, inv, coin, stats, attack_list):
        super().__init__(name, inv, coin)
        self.entity_dict['stats'] = stats
        self.entity_dict['attack_list'] = attack_list

    @property
    def stats(self):
        return self.entity_dict['stats']

    @property
    def attacks(self):
        return self.entity_dict['attack_list']

#
# Items/Weapons in the game
#


class item:
    def __init__(self, name, dscrpt, weight, val):
        self.item_dict = {}
        self.item_dict['name'] = name
        self.item_dict['description'] = dscrpt
        self.item_dict['carry_weight'] = weight
        self.item_dict['value'] = val

    @property
    def name(self):
        return self.item_dict['name']

    @property
    def dscrpt(self):
        return self.item_dict['description']

    @property
    def weight(self):
        return self.item_dict['carry_weight']

    @property
    def value(self):
        return self.item_dict['value']


class equippable(item):
    def __init__(self, name, dscrpt, weight, on_entity=False):
        super().__init__(name, dscrpt, weight)


class weapon(equippable):
    pass


class armor(equippable):
    pass


class heal_item(item):
    pass


class ranged_weapon(weapon):
    pass


class heal_magic(weapon, heal_item):
    pass

#
# Entity Stats
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
        total_weight = 0

        for i in range(len(kw['item'])):
            total_weight += kw['item'][i].weight

        if total_weight > self.calc_carry_cap():
            self.over_enc = True

#
# Locations
#


matrix_indexer = signal('matrix-indexer')


class location_manager:
    def __init__(self, maps=list(), quests=list()):
        self.xy_dict = {}
        self.xy_dict['maps'] = maps
        self.xy_dict['quests'] = quests
        for i in range(len(self.xy_dict['maps'])):
            self.xy_dict['id_directory'][i] = self.xy_dict['maps'][i].id

    def move(entity, player_position, direction):
        pass


class matrix_map:
    def __init__(self, map_id, map, entities=list()):
        self.map_dict = {}
        self.map_dict['map_id'] = map_id
        self.map_dict['map_layout'] = matrix(map)
        self.map_dict['entities'] = entities

    @matrix_indexer.connect
    def give_data(self):
        data = {}
        data['entities'] = self.entities
        data['']

    @property
    def id(self):
        return self.map_dict['map_id']

    @property
    def layout(self):
        return self.map_dict['map_layout']

    @property
    def entities(self):
        return self.map_dict['entities']

#
# Battle Backend
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
# Inventory
#


class item_collection:
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
                print("There is/are no more " + itm + " to use, sell, or buy.")

    def get_inventory(self):
        return self.items


class vendor_collection(item_collection):
    def __init__(self, items):
        super().__init__(items)

    def swap_item(self, item, swapee, count):
        if item in self.items:
            for i in range(count):
                if swapee.coin >= (item.value * count):
                    swapee.inv.add_itm(item)
                    self.rem_itm(item)
                    self.coin = item.value
                else:
                    print(swapee.name + " ran out of money.")
        else:
            print("That item doesn't exist in this inventory.")


class player_collection(vendor_collection):
    def __init__(self, items):
        super().__init__(items)

    def add_itm(self, itm, amnt=Enumerators.items_to_modify):
        for i in range(amnt):
            self.items.append(itm)
            item_obtained.send(item=self.get_inventory())


#
# Counter
#

created_entity = signal('created-entity')
created_item = signal('created-item')
created_location = signal('created-location')
created_collection = signal('created-collection')
created_quest = signal('created-quest')


class object_tracker:
    def __init__(self):
        self.track_dict = {}
        self.track_dict['entities'] = list()
        self.track_dict['items'] = list()
        self.track_dict['locations'] = list()
        self.track_dict['collections'] = list()
        self.track_dict['quests'] = list()

    @property
    def all_collections(self):
        return self.track_dict['collections']

    @created_collection.connect
    def add_collection(self, **kw):
        self.track_dict['collections'].append(kw)

# Finishing creating connect and property functions, then implement the send commands (and do it RIGHT!)
