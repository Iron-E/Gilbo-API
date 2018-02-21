from abc import ABC
from random import randint
from time import sleep
from enum import Enum


def type(phrase, waTime=.045, enTime=.5):
    for i in range(len(phrase)):
        print(phrase[i], end="", flush=True)
        sleep(waTime)

    sleep(enTime)

#
# Abstract class from which all enemies, NPCs, and players are derived.
#

class entity(ABC):
    def __init__(self, name):
        self.entity_dict = {}
        self.entity_dict['name'] = name
    @property
    def name(self):
        return self.entity_dict['name']

    @name.setter
    def name(self, value):
        self.entity_dict['name'] = value


class vendor(entity):
    def __init__(self, name, inv, coin):
        self.entity_dict['inventory'] = inv
        self.entity_dict['currency'] = coin

    @property
    def coin(self):
        return self.entity_dict['currency']

    @coin.setter
    def currency(self, value):
        self.entity_dict['currency'] += value

    @property
    def inv(self):
        return self.entity_dict['inventory']


class battler(entity):
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
    pass


class weapon(item):
    pass


class armor(item):
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

#
# Locations
#

#
# Descriptors
#
class attack:
    def __init__(self, dmg, dscrpt, count=1):
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
    def gacc(self):
        return self.attack_dict['accuracy']

#
# Inventory
#
class item_collection:
    def __init__(self, items=list()):
        self.items = items

    def add_itm(self, itm, amnt=1):
        for i in range(amnt):
            self.items.append(itm)

    def rem_itm(self, itm, amnt=1):
        for i in range(amnt):
            self.item.remove(itm)

    def get_inventory(self):
        return self.items


class vendor_collection(item_collection):
    pass
