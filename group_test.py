from player_generator import new_dict
from mythic_groups_maker import *

print("Importing dictionary ... ...")
print(new_dict)

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
print(groupsList)