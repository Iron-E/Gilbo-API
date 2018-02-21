from abc import ABC
from random import randint
from time import sleep


def type(phrase, waTime=.045, enTime=.5):
    for i in range(len(phrase)):
        print(phrase[i], end="", flush=True)
        sleep(waTime)

    sleep(enTime)


# Abstract class from which all enemies, NPCs, and players are derived.
class entity(ABC):
    def __init__(self, name):
        self.name = name


class vendor(entity):
    pass


class battler(entity):
    pass


class player(entity):
    pass


# Items/Weapons in the game
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


# Entity Stats
class battler_stats:
    stat_dict = {"hp": 0, "strength": 0, "armor": 0, "agility": 0, "power": 0}

    def __init__(self, hp, stren, armr, agil, pwr):
        self.stat_dict["hp"] = hp
        self.stat_dict["strength"] = stren
        self.stat_dict["armor"] = armr
        self.stat_dict["agility"] = agil
        self.stat_dict["power"] = pwr

    def get_stat(self, stat):
        return self.stat_dict[stat]

    def mod_stat(self, stat, value):
        self.stat_dict[stat] = value


# Locations
# Descriptors
class attack:
    def __init__(self, dmg, dscrpt):
        self.dmg = dmg
        self.dscrpt = dscrpt

    def get_dmg(self):
        return self.dmg

    def get_dscrpt(self):
        return self.dscrpt


class ranged_attack(attack):
    def __init__(self, dmg, dscrpt, ammo_cost, acc=100):
        super()
        self.acc = acc
        self.ammo_cost = ammo_cost

    def get_ammo_cost(self):
        return self.ammo_cost

    def get_acc(self):
        return self.acc


# Inventory
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
