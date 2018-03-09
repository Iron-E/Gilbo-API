# Gilbo-API
An API to design and create RPG text adventure games. Written in Python.

By using this API you agree to the [license](https://github.com/ajzett/Gilbo-API/blob/master/LICENSE.md).

## Requirements
- [blinker](https://github.com/jek/blinker/blob/master/LICENSE)
- [NumPy](https://github.com/scipy/scipy/blob/master/LICENSE.txt)
- [colorama](https://github.com/tartley/colorama/blob/master/LICENSE.txt)
- Unicode (UTF-8) support

## Features 
### Player & NPC Management
- [x] Create entities (NPCs, Players, Vendors, etc.)
- [x] Define an item list for an entity.
- [x] Define stat lists for an entity.
- [ ] Save & Load player data
- [ ] Gear based progression

### Quests & Staging
- [ ] Quests have multiple stages
- [ ] Begin quests based on events (picking up items, killing entities)
- [ ] Quest completion rewards

### Locations
The location manager defaults to working with Numpy-array-based maps and works by increasing or decreasing the player's "position" on said map, which triggers a function that reads what is on that tile. However, it can be easily modified to use other 2D, or even 3D libraries to manage a location. See [documentation](https://github.com/ajzett/Gilbo-API/blob/master/DOCUMENTATION.md) for more. 

- [ ] Location manager loads in and empties location data automatically
- [ ] Location manager feeds data to Save & Load data to the save and load functions so your character can start in the same place

### LAN Battle?
- [ ] Battle other players over LAN. Not really sure about this one.

### Modification / Structure
- Creative Commons License and Object-oriented design makes modification and redistribution easy.
- All objects (inventories, attack lists, stat lists, etc) are created independantly and then an *entity* is defined as having them. See [documentation](https://github.com/ajzett/Gilbo-API/blob/master/DOCUMENTATION.md) for more.

# Changelogs
