import Gilbo

test_map = matrix_map('eat ass')
test_map.layout = np.array([[Tiles.Grass.value, Tiles.Grass.value, Tiles.Grass.value, Tiles.Grass.value], [Tiles.Grass.value, Tiles.Building.value, Tiles.Mountain.value, Tiles.Mountain.value]])
loc_man.load_map(test_map, 4)
