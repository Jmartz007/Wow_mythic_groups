"""This module defines the Myth_Player and Wow_Char classes"""

import logging


logger = logging.getLogger(f"main.{__name__}")


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
        print(
            "Character name: "
            + self.char_name
            + "\nClass: "
            + self.wow_class
            + "\nRole(s): "
            + str(self.role)
            + "\nKey Level: "
            + str(self.key_level)
            + "\nDungeon: "
            + self.dungeon
            + "\n"
        )

    def __str__(self):
        return f"Character: {self.char_name}, {self.wow_class} - {self.key_level}, {self.dungeon} "
        # return ("Character name: " + self.char_name + ", Class: " + self.wow_class)

    def __repr__(self) -> str:
        return (
            "Character name: "
            + self.char_name
            + str(self.role)
            + " Owned by: "
            + self.playerName
        )

    def __iter__(self):
        return iter(self.__dict__.items())


###  Instantiating Myth_Players and Wow_Char
def generate_players_and_chars(players_dictionary: dict) -> list[Myth_Player]:
    # print("Generating player objects and character objects ...  ...")
    logger.info("Generating player objects and character objects ...  ...")
    players_list = []

    for player_name, characters in players_dictionary.items():
        toon_dict = {}
        toon_list = []

        for char_name, char_data in characters.items():
            toon_dict[char_name] = Wow_Char(char_name, player_name, char_data)
            logger.debug("wow_char: %s", toon_dict[char_name])
            toon_list.append(toon_dict[char_name])

        player_obj = Myth_Player(player_name, toon_list)


        logger.debug("player obj: %s", player_obj)
        players_list.append(player_obj)

    return players_list

