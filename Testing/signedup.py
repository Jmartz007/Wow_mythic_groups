playersListDB = ('Jmartz', 'Jmartz', 'Warrior', 'Tank'),('Jmartz', 'Jmartz', 'Warrior', 'DPS'),('Cardinal', 'Flashlight', 'Paladin', 'Healer'),('Cardinal', 'Fluke', 'Hunter', 'DPS'),('sajah', 'aythe', 'Warlock', 'DPS'),('sajah', 'sajah', 'Druid', 'DPS'),('sajah', 'zabella', 'Paladin', 'Tank'),('sajah', 'zabella', 'Paladin', 'DPS'),('trugbug', 'trugers', 'Rogue', 'DPS'),('ani', 'aniperson', 'Druid', 'Tank'), ('shaloo', 'shel', 'Monk', 'Tank')


pdict = {'Alduric': {'Alduric': {'Class': 'Paladin', 'Role': ['Tank', 'DPS']}}, 'ani': {'aniperson': {'Class': 'Druid', 'Role': ['Tank', 'DPS']}}, 'arrrgh': {'hitehre': {'Class': 'Priest', 'Role': ['Healer']}}, 'Cardinal': {'Flashlight': {'Class': 'Paladin', 'Role': ['Healer']}, 'Fluke': {'Class': 'Hunter', 'Role': ['DPS']}}, 'Jmartz': {'Jmartz': {'Class': 'Warrior', 'Role': ['Tank', 'DPS']}}, 'paliguy': {'pali': {'Class': 'Paladin', 'Role': ['Tank', 'DPS']}}, 'sajah': {'aythe': {'Class': 'Warlock', 'Role': ['DPS']}, 'sajah': {'Class': 'Druid', 'Role': ['DPS']}, 'zabella': {'Class': 'Paladin', 'Role': ['Tank', 'DPS']}}, 'shaloo': {'shel': {'Class': 'Monk', 'Role': ['Tank', 'Healer']}}, 'trugbug': {'trugers': {'Class': 'Rogue', 'Role': ['DPS']}}, 'warlockperson': {'pewpew': {'Class': 'Warlock', 'Role': ['DPS']}}}


# for i in range(len(playersListDB)):
#     print("---------------------------------------")
#     for j in playersListDB[i]:
#         if j ==  playersListDB[i-1][0] and j != playersListDB[i][1] :
        # if j == playersListDB[i][1]:
            # continue
            # print(f"^{j}^")
            # print(playersListDB[i][0])
        # print(playersListDB[i].index(j))
        # print(playersListDB[i-1])
        # print(f"|{j}|")
        # print(playersListDB[i-1])


# for i in range(len(pdict)):
for key, value in pdict.items():
    print("-------------------------")
    print(f"|{key}|")
    for l in range(len(value)):
        print(value)
        for k, v in value.items():
            print(f"^{k}^")
        # for k, v in value.items():
        #         print(f"^{k}^")

    # print(j)
