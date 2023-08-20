# from player_generator import new_dict
from mythic_groups_maker import *
from sqlconnector.sqlReader import sqlPlayerDict

# print(new_dict)
print("Importing dictionary ... ...")
print(sqlPlayerDict)

players_list = players_gen(sqlPlayerDict)

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
print(f"players left: {len(players_list)}")
print(players_list)
print("Max groups: " + str(p.maxGroups))
print("groups formed: " + str(len(groupsList)))
[group.verify_group() for group in groupsList]
print(startChars)
print(startPlayers)
# for group in groupsList:
#     for x in group.group_members:
#         print(x.playerName)
duplicates = [x.playerName for group in groupsList for x in group.group_members if x.playerName.count(x.playerName) > 1]
print("duplicates:")
print(duplicates)

'''
Debuggin which players are being duplicated in the group, using print statements below.

Potential fix to linking characters and players is to add a "self.playerName" attribute to the Wow_Char class and store the players name in each character

Found that the dps pool or players putting multiple dps players if they belong to one player

implement some logic which adds character to "another list", then when iterating through addmember loop, check if character is in "another list" and if so do not add character to group.
'''