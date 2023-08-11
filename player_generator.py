import random
import numpy as np
'''
example dictionary:

keystone_dict = {
    "Jmartz": {"Calioma": {"level": 7, "dungeon": "freehold", "Class": "Priest", "Role": ["Healer"]},
               "Solemartz": {"level": 3, "dungeon": "Vortex Pinnacle", "Class": "Mage", "Role": ["DPS"]},
               "Jmartz": {"level": 16, "dungeon": "Halls of Infusion", "Class": "Warrior", "Role": ["Tank", "DPS"]}},
    "Cardinal": {"Fluke": {"level": 14, "dungeon": "Underrot", "Class": "Hunter", "Role": ["DPS"]},
                 "Gael": {"level": 10, "dungeon": "Brackenhide", "Class": "Druid", "Role": ["DPS"]}},
    "Sajah": {"Sajah": {"level": 15, "dungeon": "freehold", "Class": "Druid", "Role": ["DPS"]},
              "Aythe": {"level": 7, "dungeon": "Vortex Pinnacle", "Class": "Warlock", "Role": ["DPS"]}},
    "Shelana": {"Shelager": {"level": 14, "dungeon": "Neltharus", "Class": "Monk", "Role": ["Healer"]},
                "Shelana": {"level": 12, "dungeon": "Halls of Infusion", "Class": "Shaman", "Role": ["DPS"]}},
    "Vorrox": {"Ronok": {"level": 18, "dungeon": "Underrot", "Class": "Warrior", "Role": ["DPS"]},
               "Vorrox": {"level": 7, "dungeon": "Vortex Pinnacle", "Class": "Demon Hunter", "Role": ["Tank"]},
               "Xyr": {"level": 13, "dungeon": "Neltharion's Lair", "Class": "Evoker", "Role": ["Healer", "DPS"]}}
}
'''

# lists of needed values
'''Need to add all available classes'''
dungeons = ["Vortex Pinnacle", "Freehold", "Brackenhide", "Underrot",
            "Neltharion's Lair", "Neltharus", "Halls of Infusion", "Uldaman"]
classes = ["Warrior", "Priest", "Mage", "Hunter", "Druid", "Monk",
           "Demon Hunter", "Paladin", "Warlock", "Death Knight", "Shaman"]
roles = ["Healer", "Tank", "DPS"]

# Names generator options
pre=["Shel", "Jom", "Gat", "Ver", "Sah", "Rem", "Flu", "Mar", "Vex", "Cal", "Trix"]
mid=["men", "len", "ron", "ollo", "net", "rog", "enom", "en"]
last=["sa", "en", "ian", "tan", "trax", "noma", "iel", "lana", "wa", "guan"]

def name_gen(x, *args):
    print("Generating new names... ...")
    player_names = []
    while len(player_names) < x:
        new_name = ""
        for arg in args:
            new_name = new_name + random.choice(arg)
        if new_name not in player_names:
            player_names.append(new_name)
    print(player_names)
    print(f"No of names generated: {str(len(player_names))}")
    return player_names


def key_gen():
    '''
    {"Level": 7, "Dungeon": "freehold", "Class": "Priest", "Role": ["Healer"]}
    '''
    key_dict = {}
    key_dict["Level"] = random.randint(2,20)
    key_dict["Dungeon"] = random.choice(dungeons)
    key_dict["Class"] = random.choice(classes)

    if key_dict["Class"] == "Warrior":
        key_dict["Role"] = list(np.random.choice(roles, size=random.choices([1,2], weights=[8, 2]), replace=False, p = [0, .25, .75]))
    elif key_dict["Class"] == "Priest":
        key_dict["Role"] = list(np.random.choice(roles, size=random.choices([1,2], weights=[8, 2]), replace=False, p = [0.25, 0, .75]))
    elif key_dict["Class"] == "Druid":
        key_dict["Role"] = list(np.random.choice(roles, size=random.choices([1,2, 3], weights=[7, 2, 1]), replace=False, p = [.10, .20, .70]))
    elif key_dict["Class"] == "Shaman":
        key_dict["Role"] = list(np.random.choice(roles, size=random.choices([1,2], weights=[8, 2]), replace=False, p = [0.25, 0, .75]))
    elif key_dict["Class"] == "Demon Hunter":
        key_dict["Role"] = list(np.random.choice(roles, size=random.choices([1,2], weights=[8, 2]), replace=False, p = [0, .25, .75]))
    elif key_dict["Class"] == "Paladin":
        key_dict["Role"] = list(np.random.choice(roles, size=random.choices([1,2, 3], weights=[7, 2, 1]), replace=False, p = [.10, .20, .70]))
    elif key_dict["Class"] == "Monk":
        key_dict["Role"] = list(np.random.choice(roles, size=random.choices([1,2, 3], weights=[7, 2, 1]), replace=False, p = [.10, .20, .70]))
    else:
        key_dict["Role"] = ["DPS"]

    return key_dict


def main_dict_gen(player_names, character_names):
    new_dict = {}
    for i in player_names:
        random_ints = random.randint(1,3)
        random_iters = []
        for x in range(random_ints):
            random_iters.append(random.randint(1,len(character_names)-1))
        if random_ints == 1:
            new_dict[i] = {character_names.pop(random_iters[0]): {}}
        elif random_ints == 2:
            random_iters[1] -= 1
            new_dict[i] = {character_names.pop(random_iters[0]): {}, character_names.pop(random_iters[1]): {}}
        elif random_ints == 3:
            if random_iters[1] > 1:
                random_iters[1] -= 1
            if random_iters[2] > 2:
                random_iters[2] -= 2
            new_dict[i] = {character_names.pop(random_iters[0]): {}, character_names.pop(random_iters[1]): {}, character_names.pop(random_iters[2]): {}}
    for i in new_dict:
        print(f"i is : {i}")
        for j,k in new_dict[i].items():
            k=key_gen()
            print(f"Player: {i}, Character: {j}")
            new_dict[i][j] = k
            print(f"new entry for {j}:")
            print(new_dict[i][j])
    print("New dictionary complete")
    return new_dict

# execute generate player names, character names should be players*3+1, and levels before executing the main dictionary function 

player_names = name_gen(15, pre, mid, last)
character_names = name_gen(48, pre, last)

# requires player names, character names
new_dict = main_dict_gen(player_names, character_names)
# print(new_dict)