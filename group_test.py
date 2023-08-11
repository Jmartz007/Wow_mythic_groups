from player_generator import new_dict
from mythic_groups_maker import *

print("Importing dictionary ... ...")
print(new_dict)
'''
new_dict = {'Shelrogian': {'Caltrax': {'Level': 18, 'Dungeon': 'Brackenhide', 'Class': 'Monk', 'Role': ['DPS', 'Healer']}}, 'Trixmenguan': {'Vexlana': {'Level': 4, 'Dungeon': 'Vortex Pinnacle', 'Class': 'Druid', 'Role': ['DPS']}, 'Versa': {'Level': 10, 'Dungeon': 'Freehold', 'Class': 'Paladin', 'Role': ['DPS', 'Tank']}, 'Jomsa': {'Level': 13, 'Dungeon': 'Neltharus', 'Class': 'Paladin', 'Role': ['DPS']}}, 'Remrontan': {'Gatian': {'Level': 7, 'Dungeon': 'Freehold', 'Class': 'Mage', 'Role': ['DPS']}}, 'Vexmenlana': {'Calian': {'Level': 17, 'Dungeon': "Neltharion's Lair", 'Class': 'Warlock', 'Role': ['DPS']}}, 'Marenomlana': {'Trixtan': {'Level': 4, 'Dungeon': 'Underrot', 'Class': 'Mage', 'Role': ['DPS']}, 'Remsa': {'Level': 8, 'Dungeon': 'Uldaman', 'Class': 'Warlock', 'Role': ['DPS']}}, 'Jomronian': {'Sheliel': {'Level': 6, 'Dungeon': 'Uldaman', 'Class': 'Paladin', 'Role': ['DPS']}, 'Shelsa': {'Level': 3, 'Dungeon': 'Freehold', 'Class': 'Priest', 'Role': ['DPS']}, 'Sahsa': {'Level': 12, 'Dungeon': 'Uldaman', 'Class': 'Mage', 'Role': ['DPS']}}, 'Calollowa': {'Shelwa': {'Level': 14, 'Dungeon': 'Brackenhide', 'Class': 'Paladin', 'Role': ['Tank', 'Healer', 'DPS']}}, 'Callenlana': {'Jomguan': {'Level': 17, 'Dungeon': "Neltharion's Lair", 'Class': 'Hunter', 'Role': ['DPS']}, 'Vexnoma': {'Level': 18, 'Dungeon': 'Uldaman', 'Class': 'Death Knight', 'Role': ['DPS']}, 'Jomtrax': {'Level': 17, 'Dungeon': 'Brackenhide', 'Class': 'Hunter', 'Role': ['DPS']}}, 'Remenen': {'Jomtan': {'Level': 6, 'Dungeon': 'Uldaman', 'Class': 'Warlock', 'Role': ['DPS']}, 'Sheltrax': {'Level': 18, 'Dungeon': 'Neltharus', 'Class': 'Warlock', 'Role': ['DPS']}}, 'Gatenomtan': {'Jomwa': {'Level': 7, 'Dungeon': 'Neltharus', 'Class': 'Shaman', 'Role': ['Healer']}, 'Trixian': {'Level': 4, 'Dungeon': 'Brackenhide', 'Class': 'Mage', 'Role': ['DPS']}}, 'Remnetnoma': {'Trixguan': {'Level': 13, 'Dungeon': 'Vortex Pinnacle', 'Class': 'Shaman', 'Role': ['DPS', 'Healer']}, 'Flusa': {'Level': 17, 'Dungeon': 'Brackenhide', 'Class': 
'Druid', 'Role': ['DPS']}}, 'Trixollowa': {'Vexian': {'Level': 14, 'Dungeon': 'Brackenhide', 'Class': 'Demon Hunter', 'Role': ['Tank']}}, 'Sahroniel': {'Shellana': {'Level': 14, 'Dungeon': 'Underrot', 'Class': 'Priest', 'Role': ['Healer']}}, 'Marenomsa': {'Fluiel': {'Level': 6, 'Dungeon': 'Brackenhide', 'Class': 'Death Knight', 'Role': ['DPS']}, 'Verwa': {'Level': 6, 'Dungeon': 'Halls of Infusion', 'Class': 'Warlock', 'Role': ['DPS']}, 'Gattan': {'Level': 16, 'Dungeon': 'Vortex Pinnacle', 'Class': 'Hunter', 'Role': ['DPS']}}, 'Calollotan': 
{'Sahtan': {'Level': 15, 'Dungeon': 'Halls of Infusion', 'Class': 'Death Knight', 'Role': ['DPS']}, 'Vexwa': {'Level': 12, 'Dungeon': 'Freehold', 'Class': 'Warlock', 'Role': ['DPS']}, 'Remtrax': {'Level': 20, 'Dungeon': 'Freehold', 'Class': 'Monk', 'Role': ['DPS', 'Tank']}}}'''

players_list = players_gen(new_dict)
startPlayers = f"------- NUMBER OF PLAYERS IN THE INITIAL PLAYER POOL: {len(players_list)}\n"
startChars = f"------- NUMBER OF CHARACTERS IN THE INITIAL CHARACTER POOL: {len([x.list_of_chars for x in players_list])}\n"


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
print("-----\t\t\t-----\n")
print("players left:\n" + str(players_list))
print("Max groups: " + str(p.maxGroups))
print("groups formed: " + str(len(groupsList)))
[group.verify_group() for group in groupsList]
print(startChars)
print(startPlayers)

'''
Debuggin which players are being duplicated in the group, using print statements below.

Potential fix to linking characters and players is to add a "self.playerName" attribute to the Wow_Char class and store the players name in each character

Found that the dps pool or players putting multiple dps players if they belong to one player

implement some logic which adds character to "another list", then when iterating through addmember loop, check if character is in "another list" and if so do not add character to group.
'''