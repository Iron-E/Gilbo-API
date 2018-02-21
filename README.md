# Gilbo-API
An API to design and create RPG text adventure games. Written in Python.

By using this API you agree to the [license](https://github.com/ajzett/Gilbo-API/edit/dev_ajzett/LICENSE.md).

## Requirements
- [blinker](https://github.com/jek/blinker)

## Features 
### Player & NPC Management
- [ ] Create entities (NPCs, Players, Vendors, etc.)
- [x] Define an item list for an entity.
- [x] Define stat lists for an entity.
- [ ] Save & Load player data
- [ ] Gear based progression

### Quests & Staging
- [ ] Quests have multiple stages
- [ ] Begin quests based on events (picking up items, killing entities)
- [ ] Quest completion rewards

### Locations
- [ ] Location manager loads in and empties location data automatically
- [ ] Location manager feeds data to Save & Load data to the save and load functions so your character can start in the same place

### LAN Battle?
- [ ] Battle other players over LAN. Not really sure about this one.

### Modification / Structure
- Creative Commons License and Object-oriented design makes modification and redistribution easy.
- All objects (inventories, attack lists, stat lists, etc) are created independantly and then an *entity* is defined as having them. See [documentation](https://github.com/ajzett/Gilbo-API/blob/master/DOCUMENTATION.md) for more.

# Changelogs
