from Wow_mythic_groups.MythicGroupMaker.mythic_groups_maker import players_gen, Pools

keystone_dict = {
  "Alduric": {
    "Alduric": {
      "Class": "Paladin", 
      "Hconf": 0, 
      "Role": [
        "Tank", 
        "DPS"
      ], 
      "Tconf": 0
    }
  }, 
  "Cardinal": {
    "Flashlight": {
      "Class": "Paladin", 
      "Hconf": 0, 
      "Role": [
        "Healer"
      ], 
      "Tconf": 0
    }, 
    "Fluke": {
      "Class": "Hunter", 
      "Hconf": 0, 
      "Role": [
        "DPS"
      ], 
      "Tconf": 0
    }
  }, 
  "Fern": {
    "Fernicus": {
      "Class": "Warrior", 
      "Hconf": 0, 
      "Role": [
        "Tank", 
        "DPS"
      ], 
      "Tconf": 0
    }
  }, 
  "Jmartz": {
    "Calioma": {
      "Class": "Priest", 
      "Hconf": 0, 
      "Role": [
        "Healer"
      ], 
      "Tconf": 0
    }, 
    "Jmartz": {
      "Class": "Warrior", 
      "Hconf": 0, 
      "Role": [
        "Tank", 
        "DPS"
      ], 
      "Tconf": 0
    }, 
    "TankyTank": {
      "Class": "Druid", 
      "Hconf": 0, 
      "Role": [
        "Tank"
      ], 
      "Tconf": 3
    }
  }, 
  "Shelana": {
    "Shellager": {
      "Class": "Monk", 
      "Hconf": 3, 
      "Role": [
        "Tank", 
        "Healer"
      ], 
      "Tconf": 0
    }
  }, 
  "ani": {
    "aniperson": {
      "Class": "Druid", 
      "Hconf": 0, 
      "Role": [
        "Tank", 
        "DPS"
      ], 
      "Tconf": 0
    }
  }, 
  "arrrgh": {
    "hitehre": {
      "Class": "Priest", 
      "Hconf": 3, 
      "Role": [
        "Healer"
      ], 
      "Tconf": 0
    }
  }, 
  "paliguy": {
    "pali": {
      "Class": "Paladin", 
      "Hconf": 0, 
      "Role": [
        "Tank", 
        "DPS"
      ], 
      "Tconf": 0
    }
  }, 
  "sajah": {
    "aythe": {
      "Class": "Warlock", 
      "Hconf": 0, 
      "Role": [
        "DPS"
      ], 
      "Tconf": 0
    }, 
    "sajah": {
      "Class": "Druid", 
      "Hconf": 0, 
      "Role": [
        "DPS"
      ], 
      "Tconf": 0
    }, 
    "zabella": {
      "Class": "Paladin", 
      "Hconf": 0, 
      "Role": [
        "Tank", 
        "DPS"
      ], 
      "Tconf": 0
    }
  }, 
  "shaloo": {
    "shel": {
      "Class": "Monk", 
      "Hconf": 0, 
      "Role": [
        "Tank", 
        "Healer"
      ], 
      "Tconf": 3
    }
  }, 
  "trugbug": {
    "trugers": {
      "Class": "Rogue", 
      "Hconf": 0, 
      "Role": [
        "DPS"
      ], 
      "Tconf": 0
    }
  }, 
  "warlockperson": {
    "pewpew": {
      "Class": "Warlock", 
      "Hconf": 0, 
      "Role": [
        "DPS"
      ], 
      "Tconf": 0
    }
  }
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
    # print(len(p.role))
    # print(p.playerName)
    return len((p.role))

def playercountSorting(p):
    count = 0
    for player in players_list:
        # print(player)
        # print("player -------------")
        for char in  player.list_of_chars:
            # print("char.char_name")
            # print(char.playerName)
            # print("p.char_name")
            # print(p.playerName)
        # print(p.playerName)
            # print(player.player_name)
            if p.playerName == char.playerName:
                # print("adding 1 to count")
                count += 1
                # print(count)
    # print(count)
    return count

newlist = [1,2,3,4,5]

def competencysorting(p):
    print(p.hConf)
    return p.hConf

# newlist.sort(key=lambda p: (competencysorting(p)))

print(newlist)

print("before sorting")
print(p.healerPool)
before = p.healerPool.copy()

# p.healerPool.sort(key=lambda p: (playercountSorting(p), roleSorting(p), competencysorting(p)))

# print("before sorting")
# print(before)
print("after")
print(p.healerPool)

# print("before sorting")
# print(p.tankPool)

# p.tankPool.sort(key=roleSorting)
# print("after sorting")
# print( p.tankPool)

# print("before sorting")
# print(p.healerPool)
# p.healerPool.sort(key=lambda e:(e.role))
# print("after sorting")
# print(p.healerPool)

def competencysorting(p):
    return p


newlist.sort(key=lambda p: competencysorting(p), reverse=True)

print(newlist)


{'Callenguan': {'Caliel': {'Level': 4, 'Dungeon': 'Underrot', 'Class': 'Mage', 'Role': ['DPS']}}, 'Trixrontan': {'Remian': {'Level': 14, 'Dungeon': "Neltharion's Lair", 'Class': 'Death Knight', 'Role': ['DPS']}}, 'Gatollotrax': {'Gatguan': {'Level': 16, 'Dungeon': 'Freehold', 'Class': 'Monk', 'Role': ['DPS', 'Healer']}}, 'Jomollolana': {'Trixsa': {'Level': 16, 'Dungeon': 'Underrot', 'Class': 'Mage', 'Role': ['DPS']}}, 'Gatlentrax': {'Shelen': {'Level': 5, 'Dungeon': 'Freehold', 'Class': 'Druid', 'Role': ['DPS']}, 'Flunoma': {'Level': 16, 'Dungeon': 'Brackenhide', 'Class': 'Shaman', 'Role': ['DPS']}, 'Remen': {'Level': 3, 'Dungeon': 'Brackenhide', 'Class': 'Druid', 'Role': ['DPS']}}, 'Gatrogwa': {'Caltan': {'Level': 19, 'Dungeon': 'Brackenhide', 'Class': 'Demon Hunter', 'Role': ['DPS']}, 'Verian': {'Level': 4, 'Dungeon': 'Halls of Infusion', 'Class': 'Paladin', 'Role': ['DPS']}, 'Sahnoma': {'Level': 16, 'Dungeon': 'Brackenhide', 'Class': 'Druid', 'Role': ['DPS']}}, 'Vexronlana': {'Veriel': {'Level': 16, 'Dungeon': 'Freehold', 'Class': 'Death Knight', 'Role': ['DPS']}, 'Vernoma': {'Level': 6, 'Dungeon': "Neltharion's Lair", 'Class': 'Death Knight', 'Role': ['DPS']}}, 'Remennoma': {'Trixtan': {'Level': 11, 'Dungeon': 'Vortex Pinnacle', 'Class': 'Druid', 'Role': ['DPS']}, 'Trixlana': {'Level': 5, 'Dungeon': 'Underrot', 'Class': 'Priest', 'Role': ['DPS']}, 'Vextan': {'Level': 20, 'Dungeon': 'Underrot', 'Class': 'Warlock', 'Role': ['DPS']}}, 'Shelenomtrax': {'Maren': {'Level': 9, 'Dungeon': 'Freehold', 'Class': 'Demon Hunter', 'Role': ['DPS']}}, 'Jomneten': {'Sheliel': {'Level': 12, 'Dungeon': 'Uldaman', 'Class': 'Shaman', 'Role': ['DPS', 'Healer']}, 'Callana': {'Level': 6, 'Dungeon': 'Uldaman', 'Class': 'Mage', 
'Role': ['DPS']}, 'Sahtrax': {'Level': 16, 'Dungeon': 'Neltharus', 'Class': 'Hunter', 'Role': ['DPS']}}}