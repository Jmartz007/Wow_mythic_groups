from player_generator import new_dict
from mythic_groups_maker import *

print("Importing dictionary ... ...")
print(new_dict)

players_list = players_gen(new_dict)

tanks = tank_pool(players_list)
healers = healer_pool(players_list)
dpsers = dps_pool(players_list)

max_g, max_t, max_h, max_dps = max_groups(players_list, tanks, healers, dpsers)

groupsList = AddMembers.get_tanks(players_list, tanks, max_t)


print_all_players(players_list)
print(groupsList[0].tank)