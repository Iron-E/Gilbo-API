import Gilbo as G


# Test map class
class test_matrix_map(G.array_map):
    def __init__(self, name):
        super().__init__(name)

    def send_data(self, tile, plyr=False):
        return True


# Test maps
test1 = test_matrix_map('tortelini')
test2 = test_matrix_map('tortelini')
test1.layout = G.np.array([[G.Tiles.Grass, G.Tiles.Grass, G.Tiles.Grass, G.Tiles.Grass], [G.Tiles.Grass, G.Tiles.Building, G.Tiles.Mountain, G.Tiles.Mountain]])
test2.layout = G.np.array([[G.Tiles.Cave, G.Tiles.Water, G.Tiles.Building, G.Tiles.Building], [G.Tiles.Dirt, G.Tiles.Ice, G.Tiles.Wall, G.Tiles.Lava]])

# Items
test_debuff = G.buff_item('Test Debuff', 'Debuff to Test use_debuff()', 0, 5, 0, 0, -10)
use_test_debuff = G.item('debuff_player() Ammo', 'Item to use debuff_player()', 0)

# Attacks
smash = G.attack('Basic Smash', 'You use your entire body to smash the opponent.', 15)
debuff_player = G.ammo_attack('Debuff Test', "Debuff target's armor.", 8, use_test_debuff, 1, 100, 1, test_debuff)

# Weapons
doodle = G.weapon('Wackadoodle', 'A mysterious doodle of some kind. Wacky.', 5, 15, [smash], 5)
diddle = G.weapon('Wacky Test Diddle', 'A dubious test item.', 10, 40, [smash, debuff_player])

# Define Player
jim_stats = G.battler_stats(50, 30, 45, 20, 1)
jim_collection = G.player_collection(20, [doodle], [doodle])
jim = G.player('Jimbo', test1, 2, 1, jim_collection, jim_stats)

# Define Test Enemy
test_enemy_stats = G.battler_stats(50, 45, 10, 50, 100)
test_enemy_collection = G.battler_collection(20, [diddle, use_test_debuff, use_test_debuff], [diddle])
test_enemy = G.battler('Enemy', test1, 2, 1, test_enemy_collection, test_enemy_stats)

# Battle jim and test_enemy
G.bat_man.battle(jim, test_enemy)
