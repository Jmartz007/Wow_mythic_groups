

#%% Data
keystone_dict = {"Jmartz": {"Calioma" : {"level": 7, "dungeon": "freehold", "Class": "Priest", "Role": ["Healer"]},
                            "Solemartz": {"level": 3, "dungeon": "Vortex Pinnacle", "Class": "Mage", "Role": ["DPS"]},
                            "Jmartz": {"level": 16, "dungeon": "Halls of Infusion", "Class": "Warrior", "Role": ["Tank", "DPS"]}},
                "Cardinal": {"Fluke" : {"level": 14, "dungeon": "Underrot", "Class": "Hunter", "Role": ["DPS"]},
                             "Gael" : {"level": 10, "dungeon": "Brackenhide", "Class": "Druid", "Role": ["DPS"]}}}

#%% Classes 
class Myth_Player:
    def __init__(self, player, char_list):
        self.player_name = player
        self.list_of_chars = char_list
        self.string_list_of_chars = [x.char_name for x in char_list]
    
    def print_character_list(self):
        '''Prints all characters from all players in the pool'''
        print(f"{self.player_name} has the following characters: \n")
        for i in self.list_of_chars:
            print(i)

    def __str__(self):
        return self.player_name + " has the following characters:" + str(self.string_list_of_chars)

class Wow_Char:
    def __init__(self,name, char_dict):
        self.char_name = name
        self.wow_class = char_dict["Class"]
        self.role = char_dict["Role"]
        self.key_level = char_dict["level"]
        self.dungeon = char_dict["dungeon"]
    
    def __str__(self):
        return ("Character name: " + self.char_name + "\nClass: " + self.wow_class + "\nRole(s): " + str(self.role) +
                "\nKey Level: " + str(self.key_level)
                + "\nDungeon: " + self.dungeon + "\n")

#%% Printing Helper Functions
def print_all_players():
    '''Prints all players signed up'''
    print("List of all players: ")
    for i in range(len(players_list)):
        print(players_list[i])

def print_all_characters():
    '''Prints all characters from all players in the pool'''
    print("List of all characters and keys: ")
    for i in players_list:
        for x in i.list_of_chars:
            print(x)


players_list = []

for i in keystone_dict:
    char_list = list(keystone_dict[i].keys())
    # print(i) ## Player names ie: Jmartz
    # print(char_list) ## Character names ie: Calioma
    toon_list = []
    for num in char_list:
        locals()[num] = Wow_Char(num, keystone_dict[i][num])  # create an instance of the character object
        toon_list.append(locals()[num])
    locals()[i] = Myth_Player(i, toon_list)  # Create an instance of the player object with the list of character objects
    players_list.append(locals()[i])

print_all_players()
print("\n")
print_all_characters()
print("\n")
Jmartz.print_character_list() # Print an ind players characters
print(Jmartz)

#%% Matchmaking
class Group:
    def __init__(self):
        self.group_members = []
        self.tank = []
        self.healer = []
        self.dps = []
    
    def add_group_member(self, character):
        self.group_members.append(character)

    def verify_group(self):
        if self.tank is not None and self.healer is not None and len(self.dps) == 3:
            return True
        else:
            False
