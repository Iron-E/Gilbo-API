from abc import ABC, abstractmethod
from random import *
from time import sleep

def rndNum(high, low = 1):
    return random.randint(low, high)

def type(phrase, waTime = 40, enTime = 500):
    print("\n")
    for i in enumerate(phrase):
        print(i[1], end='')
        sleep(waTime)

    sleep(enTime)

# Abstract class from which all enemies, bosses, vendors, NPCs, and players are derived.
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

# Descriptors
