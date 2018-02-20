from abc import ABC, abstractmethod
from random import *

def rndNum(high, low = 1):
    return randint(low, high)

def type(phrase):
    pass

# Abstract class from which all enemies, bosses, vendors, NPCs, and players are derived.
class entity(ABC):
    def __init__(self, name):
        self.name = name

    def say(phrase):
        pass
