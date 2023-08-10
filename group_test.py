# from player_generator import new_dict
from mythic_groups_maker import *

# print(new_dict)
print("Importing dictionary ... ...")
new_dict = {'Calenomnoma': {'Jomtan': {'Level': 12, 'Dungeon': 'Freehold', 'Class': 'Mage', 'Role': ['DPS']}}, 'Remrogiel': {'Vexen': {'Level': 12, 'Dungeon': 'Brackenhide', 'Class': 'Death Knight', 'Role': ['DPS']}, 'Vextrax': {'Level': 13, 'Dungeon': "Neltharion's Lair", 'Class': 'Paladin', 'Role': ['Healer']}, 'Sahnoma': {'Level': 16, 'Dungeon': 'Uldaman', 'Class': 'Warlock', 'Role': ['DPS']}}, 'Shelenomwa': {'Vernoma': {'Level': 4, 'Dungeon': "Neltharion's Lair", 'Class': 'Priest', 'Role': ['DPS']}, 'Jomwa': {'Level': 19, 'Dungeon': 'Brackenhide', 'Class': 'Mage', 'Role': ['DPS']}}, 'Shelmennoma': {'Marian': {'Level': 5, 'Dungeon': 'Neltharus', 'Class': 'Priest', 'Role': ['DPS']}, 'Sahwa': {'Level': 20, 'Dungeon': 'Brackenhide', 'Class': 'Death Knight', 'Role': ['DPS']}, 'Remtan': {'Level': 18, 'Dungeon': "Neltharion's Lair", 'Class': 'Shaman', 'Role': ['Healer']}}, 'Shellentrax': {'Jomiel': {'Level': 9, 'Dungeon': 'Halls of Infusion', 'Class': 'Mage', 'Role': ['DPS']}}, 'Vermeniel': {'Sheliel': {'Level': 18, 'Dungeon': 'Halls of Infusion', 'Class': 'Death Knight', 'Role': ['DPS']}}, 'Marronnoma': {'Fluian': {'Level': 10, 'Dungeon': 'Halls of Infusion', 'Class': 'Hunter', 'Role': ['DPS']}, 'Sheltrax': {'Level': 15, 'Dungeon': 'Uldaman', 'Class': 'Warlock', 'Role': ['DPS']}, 'Remiel': {'Level': 11, 'Dungeon': 'Brackenhide', 'Class': 'Shaman', 'Role': ['DPS']}}, 'Trixronsa': {'Vexguan': {'Level': 9, 'Dungeon': 'Underrot', 'Class': 'Hunter', 'Role': ['DPS']}, 'Jomnoma': {'Level': 11, 'Dungeon': 'Uldaman', 'Class': 'Mage', 'Role': ['DPS']}, 'Remian': {'Level': 11, 'Dungeon': 'Halls of Infusion', 'Class': 'Death Knight', 'Role': ['DPS']}}, 'Vexnetguan': {'Veren': {'Level': 4, 'Dungeon': 'Underrot', 'Class': 'Warrior', 'Role': ['Tank']}, 'Sahsa': {'Level': 6, 'Dungeon': 'Vortex Pinnacle', 'Class': 'Priest', 'Role': ['Healer']}, 'Remlana': {'Level': 6, 'Dungeon': 'Halls of Infusion', 'Class': 'Mage', 'Role': ['DPS']}}, 'Calenomwa': {'Remguan': {'Level': 20, 'Dungeon': 'Brackenhide', 'Class': 'Mage', 'Role': ['DPS']}}, 'Vexenlana': {'Marwa': {'Level': 15, 'Dungeon': "Neltharion's Lair", 'Class': 'Warlock', 'Role': ['DPS']}}, 'Vexlentan': {'Shelwa': {'Level': 12, 'Dungeon': 'Underrot', 'Class': 'Shaman', 'Role': ['DPS']}}, 'Gatrontrax': {'Trixtrax': {'Level': 18, 'Dungeon': 'Uldaman', 
'Class': 'Warlock', 'Role': ['DPS']}, 'Flutrax': {'Level': 12, 'Dungeon': 'Vortex Pinnacle', 'Class': 'Demon Hunter', 'Role': ['Tank']}, 'Gatnoma': {'Level': 2, 'Dungeon': 'Uldaman', 'Class': 'Priest', 'Role': ['Healer']}}, 'Verlensa': {'Jomsa': {'Level': 20, 'Dungeon': 'Uldaman', 'Class': 'Warlock', 'Role': ['DPS']}, 'Sheltan': {'Level': 16, 'Dungeon': 'Freehold', 'Class': 'Paladin', 'Role': ['DPS']}}, 'Shelnetiel': {'Versa': {'Level': 20, 'Dungeon': 'Brackenhide', 'Class': 'Warlock', 'Role': ['DPS']}, 'Calwa': {'Level': 10, 'Dungeon': 'Vortex Pinnacle', 'Class': 'Warlock', 'Role': ['DPS']}}}


players_list = players_gen(new_dict)

p = Pools(players_list)
p.tank_pool()
p.healer_pool()
p.dps_pool()
p.max_groups()

groupsList = AddMembers.get_tanks(p)

print_all_players(players_list)
print(len(players_list))

AddMembers.get_healer(p, groupsList)

print(players_list)
print(len(players_list))
print("\n")

AddMembers.get_dps(p, groupsList)
print(groupsList)
print("players left:\n" + str(players_list))
print("Max groups: " + str(p.maxGroups))

# need to fix 3 players remaining when there should be 0