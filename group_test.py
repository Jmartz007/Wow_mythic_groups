# from player_generator import new_dict
from mythic_groups_maker import *
from sqlReader import sqlPlayerDict

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
print("players left:\n" + str(players_list))
print("Max groups: " + str(p.maxGroups))

# need to fix 3 players remaining when there should be 0