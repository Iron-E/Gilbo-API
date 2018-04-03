import Gilbo as G

test_map = G.matrix_map('eat ass')
test_map.layout = G.np.array([[G.Tiles.Grass.value, G.Tiles.Grass.value, G.Tiles.Grass.value, G.Tiles.Grass.value], [G.Tiles.Grass.value, G.Tiles.Building.value, G.Tiles.Mountain.value, G.Tiles.Mountain.value]])
G.loc_man.load_map(test_map, 4)

smash = G.attack(100, 'You use your entire body to smash the opponent.')
doodle = G.weapon('Wackadoodle', 'A mysterious doodle of some kind. Wacky.', 5, 100, 5, [smash])
jim_collection = G.player_collection([doodle], [doodle])
jim_stats = G.player_stats(50, 100, 10, 30, 100)
jim = G.player('Jimbo', test_map, 1, 2, jim_collection, 20, jim_stats)

new_item = jim.collection.inventory[0].__class__.__mro__[2]('you', 'suck', 20, 20)
print(jim.collection.inventory[0].__class__.__mro__)
if G.item_weighted in jim.collection.inventory[0].__class__.__mro__:
    print('true\n')
else:
    print('false\n')

import inspect
G.tracker.update_tracker(inspect.getfile(inspect.currentframe()))
print(G.tracker.tracker)
