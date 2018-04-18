import Gilbo as G


class test_matrix_map(G.matrix_map):
    def __init__(self, name):
        super().__init__(name)

    def send_data(self, tile):
        if tile[0] == 0:
            print('You are on the first level.')
            return True
        else:
            print('You are on the second level.')
            return True


test_map = test_matrix_map('tortelini')
test_map.layout = G.np.array([[G.Tiles.Grass.value, G.Tiles.Grass.value, G.Tiles.Grass.value, G.Tiles.Grass.value], [G.Tiles.Grass.value, G.Tiles.Building.value, G.Tiles.Mountain.value, G.Tiles.Mountain.value]])

smash = G.attack(100, 'You use your entire body to smash the opponent.')
doodle = G.weapon('Wackadoodle', 'A mysterious doodle of some kind. Wacky.', 5, 100, 5, [smash])
jim_collection = G.player_collection([doodle], [doodle])
jim_stats = G.player_stats(50, 100, 10, 30, 100)
jim = G.player('Jimbo', test_map, 2, 1, jim_collection, 20, jim_stats)

G.loc_man.load_map(test_map)

# G.tracker.update_tracker(globals())

G.loc_man.move(jim, G.Directions.Up)
