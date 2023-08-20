from mythic_groups_maker import players_gen, Pools

keystone_dict = {
                "Jmartz": {"Calioma" : {"Level": 7, "Dungeon": "freehold", "Class": "Priest", "Role": ["Healer"]},
                        "Solemartz": {"Level": 3, "Dungeon": "Vortex Pinnacle", "Class": "Mage", "Role": ["DPS"]},
                        "Jmartz": {"Level": 16, "Dungeon": "Halls of Infusion", "Class": "Warrior", "Role": ["Tank", "DPS"]}},
                "Cardinal": {"Fluke" : {"Level": 14, "Dungeon": "Underrot", "Class": "Hunter", "Role": ["DPS"]},
                        "Gael" : {"Level": 10, "Dungeon": "Brackenhide", "Class": "Druid", "Role": ["DPS"]},
                    "Flashlight" : {"Level": 10, "Dungeon": "Brackenhide", "Class": "Paladin", "Role": ["Tank, Healer"]}},
                "Sajah": {"Sajah" : {"Level": 15, "Dungeon": "freehold", "Class": "Druid", "Role": ["DPS"]},
                        "Aythe": {"Level": 7, "Dungeon": "Vortex Pinnacle", "Class": "Warlock", "Role": ["DPS"]}},
                "Vorrox": {"Ronok" : {"Level": 18, "Dungeon": "Underrot", "Class": "Warrior", "Role": ["DPS"]},
                        "Vorrox": {"Level": 7, "Dungeon": "Vortex Pinnacle", "Class": "Demon Hunter", "Role": ["Tank"]},
                        "Xyr" : {"Level": 13, "Dungeon": "Neltharion's Lair", "Class": "Evoker", "Role": ["Healer", "DPS"]}},
                "Shelana": {"Shelager" : {"Level": 14, "Dungeon": "Neltharus", "Class": "Monk", "Role": ["Healer"]},
                        "Shelana": {"Level": 12, "Dungeon": "Halls of Infusion", "Class": "Shaman", "Role": ["DPS"]}}
                        }

players_list = players_gen(keystone_dict)

p = Pools(players_list)

# tanks = tank_pool(players_list)
p.tank_pool()
# healers = healer_pool(players_list)
p.healer_pool()
# dpsers = dps_pool(players_list)
p.dps_pool()

# max_g, max_t, max_h, max_dps = max_groups(players_list,tanks, healers, dpsers)
p.max_groups()

def roleSorting(p):
    return len((p.role))
# print(p.tankPool)

for wowchar in  p.tankPool:
    print(len(wowchar.role))
    print(wowchar.role)

p.healerPool.sort(key=roleSorting)

# for healer in p.healerPool:
#     print(healer)

print("before sorting")
print(p.tankPool)

p.tankPool.sort(key=roleSorting)
print("after sorting")
print( p.tankPool)

print("before sorting")
print(p.healerPool)
p.healerPool.sort(key=roleSorting)
print("after sorting")
print(p.healerPool)


{'Callenguan': {'Caliel': {'Level': 4, 'Dungeon': 'Underrot', 'Class': 'Mage', 'Role': ['DPS']}}, 'Trixrontan': {'Remian': {'Level': 14, 'Dungeon': "Neltharion's Lair", 'Class': 'Death Knight', 'Role': ['DPS']}}, 'Gatollotrax': {'Gatguan': {'Level': 16, 'Dungeon': 'Freehold', 'Class': 'Monk', 'Role': ['DPS', 'Healer']}}, 'Jomollolana': {'Trixsa': {'Level': 16, 'Dungeon': 'Underrot', 'Class': 'Mage', 'Role': ['DPS']}}, 'Gatlentrax': {'Shelen': {'Level': 5, 'Dungeon': 'Freehold', 'Class': 'Druid', 'Role': ['DPS']}, 'Flunoma': {'Level': 16, 'Dungeon': 'Brackenhide', 'Class': 'Shaman', 'Role': ['DPS']}, 'Remen': {'Level': 3, 'Dungeon': 'Brackenhide', 'Class': 'Druid', 'Role': ['DPS']}}, 'Gatrogwa': {'Caltan': {'Level': 19, 'Dungeon': 'Brackenhide', 'Class': 'Demon Hunter', 'Role': ['DPS']}, 'Verian': {'Level': 4, 'Dungeon': 'Halls of Infusion', 'Class': 'Paladin', 'Role': ['DPS']}, 'Sahnoma': {'Level': 16, 'Dungeon': 'Brackenhide', 'Class': 'Druid', 'Role': ['DPS']}}, 'Vexronlana': {'Veriel': {'Level': 16, 'Dungeon': 'Freehold', 'Class': 'Death Knight', 'Role': ['DPS']}, 'Vernoma': {'Level': 6, 'Dungeon': "Neltharion's Lair", 'Class': 'Death Knight', 'Role': ['DPS']}}, 'Remennoma': {'Trixtan': {'Level': 11, 'Dungeon': 'Vortex Pinnacle', 'Class': 'Druid', 'Role': ['DPS']}, 'Trixlana': {'Level': 5, 'Dungeon': 'Underrot', 'Class': 'Priest', 'Role': ['DPS']}, 'Vextan': {'Level': 20, 'Dungeon': 'Underrot', 'Class': 'Warlock', 'Role': ['DPS']}}, 'Shelenomtrax': {'Maren': {'Level': 9, 'Dungeon': 'Freehold', 'Class': 'Demon Hunter', 'Role': ['DPS']}}, 'Jomneten': {'Sheliel': {'Level': 12, 'Dungeon': 'Uldaman', 'Class': 'Shaman', 'Role': ['DPS', 'Healer']}, 'Callana': {'Level': 6, 'Dungeon': 'Uldaman', 'Class': 'Mage', 
'Role': ['DPS']}, 'Sahtrax': {'Level': 16, 'Dungeon': 'Neltharus', 'Class': 'Hunter', 'Role': ['DPS']}}}