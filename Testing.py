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

# Stuff for Jimbo
smash = G.attack('Basic Smash', 15, 'You use your entire body to smash the opponent.')
doodle = G.weapon('Wackadoodle', 'A mysterious doodle of some kind. Wacky.', 5, 100, [smash], 5)
diddle = G.weapon('Wackadoodle', 'A mysterious doodle of some kind. Wacky.', 5, 100, [smash], 5)
jim_collection = G.player_collection(20, [doodle], [doodle])
test_enemy_collection = G.battler_collection(20, [doodle], [doodle])
jim_stats = G.battler_stats(50, 100, 20, 30, 10)
test_enemy_stats = G.battler_stats(50, 45, 10, 50, 100)
jim = G.player('Jimbo', test1, 2, 1, jim_collection, jim_stats)
test_enemy = G.player('Enemy', test1, 2, 1, test_enemy_collection, test_enemy_stats)

G.loc_man.load_map(test1)

G.tracker.update_tracker(globals())

G.loc_man.move(jim, G.Directions.Up)
G.loc_man.teleport(jim, test2, 2, 0)
G.loc_man.move(jim, G.Directions.Left)

G.bat_man.battle(jim, test_enemy)
