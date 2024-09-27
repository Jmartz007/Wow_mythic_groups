'''This module defines the Myth_Player and Wow_Char classes'''
import logging


logger = logging.getLogger(f"main.{__name__}")

### Data for testing
keystone_dict = {
                "Jmartz": {"Calioma" : {"Level": 7, "Dungeon": "freehold", "Class": "Priest", "Role": ["Healer"]},
                        "Solemartz": {"Level": 3, "Dungeon": "Vortex Pinnacle", "Class": "Mage", "Role": ["DPS"]},
                        "Jmartz": {"Level": 16, "Dungeon": "Halls of Infusion", "Class": "Warrior", "Role": ["Tank", "DPS"]}},
                "Cardinal": {"Fluke" : {"Level": 14, "Dungeon": "Underrot", "Class": "Hunter", "Role": ["DPS"]},
                        "Gael" : {"Level": 10, "Dungeon": "Brackenhide", "Class": "Druid", "Role": ["DPS"]},
                    "Flashlight" : {"Level": 10, "Dungeon": "Brackenhide", "Class": "Paladin", "Role": ["Tank, Healer"]}},
                "Sajah": {"Sajah" : {"Level": 15, "Dungeon": "freehold", "Class": "Druid", "Role": ["DPS"]},
                        "Aythe": {"Level": 7, "Dungeon": "Vortex Pinnacle", "Class": "Warlock", "Role": ["DPS"]}},
                "Shelana": {"Shelager" : {"Level": 14, "Dungeon": "Neltharus", "Class": "Monk", "Role": ["Healer"]},
                        "Shelana": {"Level": 12, "Dungeon": "Halls of Infusion", "Class": "Shaman", "Role": ["DPS"]}},
                "Vorrox": {"Ronok" : {"Level": 18, "Dungeon": "Underrot", "Class": "Warrior", "Role": ["DPS"]},
                        "Vorrox": {"Level": 7, "Dungeon": "Vortex Pinnacle", "Class": "Demon Hunter", "Role": ["Tank"]},
                        "Xyr" : {"Level": 13, "Dungeon": "Neltharion's Lair", "Class": "Evoker", "Role": ["Healer", "DPS"]}}
                        }


### Player and Character Classes 
class Myth_Player:
    """This class serves as a container for Wow_Char objects"""
    def __init__(self, player, char_list):
        self.player_name = player
        self.list_of_chars = char_list
        self.string_list_of_chars = [x.char_name for x in char_list]
    
    def print_character_list(self):
        print(f"{self.player_name} has the following characters: \n")
        for i in self.list_of_chars:
            print(i)

    def __str__(self):
        return self.player_name
    
    def __repr__(self) -> str:
        return "Player: " + self.player_name

class Wow_Char:
    def __init__(self, name, playerName, char_dict):
        self.playerName = playerName
        self.char_name = name
        self.wow_class = char_dict["Class"]
        self.role = char_dict["Role"]
        self.range = char_dict["Range"]
        self.hConf = char_dict.get("Healer Skill")
        self.tConf = char_dict.get("Tank Skill")
        self.dpsConf = char_dict.get("DPS Skill")
        self.key_level = char_dict["Key Level"]
        self.dungeon = char_dict["Dungeon"]
        self.is_active = char_dict["is_active"]
    
    def print_character_info(self):
        print("Character name: " + self.char_name + "\nClass: " + self.wow_class + "\nRole(s): " + str(self.role) + "\nKey Level: " + str(self.key_level) + "\nDungeon: " + self.dungeon + "\n")

    def __str__(self):
        return f"Character: {self.char_name}, {self.wow_class} - {self.key_level}, {self.dungeon} "
        # return ("Character name: " + self.char_name + ", Class: " + self.wow_class)
    
    def __repr__(self) -> str:
        return "Character name: " + self.char_name + str(self.role) + " Owned by: " + self.playerName


###  Instantiating Myth_Players and Wow_Char
def generate_players_and_chars(players_dictionary:dict) -> list[Myth_Player]:
    # print("Generating player objects and character objects ...  ...")
    logger.info("Generating player objects and character objects ...  ...")
    players_list = []
    for i in players_dictionary:
        char_list = list(players_dictionary[i].keys())
        # print(i) ## Player names ie: Jmartz
        # print(char_list) ## Character names ie: Calioma
        toon_list = []
        for num in char_list:
            locals()[num] = Wow_Char(num, i, players_dictionary[i][num])  # create an instance of the character object
            toon_list.append(locals()[num])
        locals()[i] = Myth_Player(i, toon_list)  # Create an instance of the player object with the list of character objects
        players_list.append(locals()[i])
    return players_list

