from player_generator import new_dict
from mythic_groups_maker import *

print("Importing dictionary ... ...")
print(new_dict)

players_list = players_gen(new_dict)

tanks = tank_pool(players_list)
healers = healer_pool(players_list)
dpsers = dps_pool(players_list)

max_g, max_t, max_h, max_dps = max_groups(players_list, tanks, healers, dpsers)



""" def test_new_group():
    print("before groups")
    print_all_players()
    print("---")
    g1 = Group()
    print(">>Created new group: " + "g1<<")
    g1.request_member(players_list)
    print("requesting new member ...")
    print("group 1 after memeber1 added:")
    print(g1)
    print("player list after Group member request 1")
    print_all_players()
    print("---")
    print("g1 dps list length")
    print(len(g1.dps))
    if len(g1.dps) < 3:
        print("less than 3 dps")

def test_add_member(number):
    print("requesting new member " + str(number) + "...")
    g1.request_member(players_list)
    print("g1 dps list:")
    print(g1.dps)
    print("group 1 member list after request 2:")
    print(g1)
    print("After Group")
    print_all_players()
 """