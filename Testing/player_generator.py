import random
'''
example dictionary:
'''
keystone_dict = {
                "Jmartz": {"Calioma" : {"level": 7, "dungeon": "freehold", "Class": "Priest", "Role": ["Healer"]},
                        "Solemartz": {"level": 3, "dungeon": "Vortex Pinnacle", "Class": "Mage", "Role": ["DPS"]},
                        "Jmartz": {"level": 16, "dungeon": "Halls of Infusion", "Class": "Warrior", "Role": ["Tank", "DPS"]}},
                "Cardinal": {"Fluke" : {"level": 14, "dungeon": "Underrot", "Class": "Hunter", "Role": ["DPS"]},
                        "Gael" : {"level": 10, "dungeon": "Brackenhide", "Class": "Druid", "Role": ["DPS"]}},
                "Sajah": {"Sajah" : {"level": 15, "dungeon": "freehold", "Class": "Druid", "Role": ["DPS"]},
                        "Aythe": {"level": 7, "dungeon": "Vortex Pinnacle", "Class": "Warlock", "Role": ["DPS"]}},
                "Shelana": {"Shelager" : {"level": 14, "dungeon": "Neltharus", "Class": "Monk", "Role": ["Healer"]},
                        "Shelana": {"level": 12, "dungeon": "Halls of Infusion", "Class": "Shaman", "Role": ["DPS"]}},
                "Vorrox": {"Ronok" : {"level": 18, "dungeon": "Underrot", "Class": "Warrior", "Role": ["DPS"]},
                        "Vorrox": {"level": 7, "dungeon": "Vortex Pinnacle", "Class": "Demon Hunter", "Role": ["Tank"]},
                        "Xyr" : {"level": 13, "dungeon": "Neltharion's Lair", "Class": "Evoker", "Role": ["Healer", "DPS"]}}
                        }


new_dict = {}

player_names = []
character_names = []
dungeons = ["Vortex Pinnacle", "Freehold", "Brackenhide", "Underrot", "Neltharion's Lair", "Neltharus", "Halls of Infusion", "Uldaman"]
levels = random.randint(1,20)
classes = ["Warrior", "Priest", "Mage", "Hunter", "Druid", "Monk", "Demon Hunter", "Paladin", "Warlock", "Death Knight", "Shaman"]
roles = ["Healer", "Tank", "DPS"]

print(levels)
