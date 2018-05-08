# Gilbo-API
An API to design and create RPG text adventure games. Written in Python.

By using this API you agree to the [license](https://github.com/ajzett/Gilbo-API/blob/master/LICENSE.md), and the licenses of the requirements.

## Dependencies
- [django dispatch](https://github.com/django/django/blob/master/django/dispatch/license.txt)
- [NumPy](https://github.com/scipy/scipy/blob/master/LICENSE.txt)*
- [colorama](https://github.com/tartley/colorama/blob/master/LICENSE.txt)
- [dill](https://github.com/uqfoundation/dill/blob/master/LICENSE)*
- Unicode (UTF-8) support (if you use the built-in graphics)

*Must be downloaded separately.

You can install `NumPy` and `dill` by entering a command-line or terminal interface, and passing the following commands to pip:
```
pip install numpy
pip install dill
```

By using Gilbo's dependencies, you agree to their licenses.

## Features 
### Player & NPC Management
- [x] Create entities (NPCs, Players, Vendors, etc.)
- [x] Define an item list for an entity.
- [x] Define stat lists for an entity.
- [x] Basic Save & Load data
- [x] Gear based progression system
- [ ] Battle entities.

### Quests & Staging
- [x] Quests have multiple stages
- [x] Begin quests based on events (picking up items, killing entities)
- [x] Quest completion rewards

### Locations
The location manager defaults to working with Numpy-array-based maps and works by increasing or decreasing the player's "position" on said map, which triggers a function that reads what is on that tile. However, it can be easily modified to use other 2D, or even 3D libraries to manage a location. See [documentation](https://github.com/ajzett/Gilbo-API/blob/master/DOCUMENTATION.md) for more. 

- [x] Location manager loads in and empties location data automatically
- [x] Location manager feeds data to Save & Load data to the save and load functions so your character can start in the same place

### LAN Battle?
- [ ] Battle other players over LAN. Not really sure about this one.

### Modification / Structure
- Creative Commons License and Object-oriented design allows for easy utilization or modification, and permits redistribution.

# Changelogs
None until release.
