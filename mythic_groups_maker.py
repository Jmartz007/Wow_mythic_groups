

#%% Data
keystone_dict = {
                "Jmartz": {"Calioma" : {"level": 7, "dungeon": "freehold",
                        "Class": "Priest", "Role": ["Healer"]},
                        "Solemartz": {"level": 3, "dungeon": "Vortex Pinnacle", "Class": "Mage", "Role": ["DPS"]},
                        "Jmartz": {"level": 16, "dungeon": "Halls of Infusion", "Class": "Warrior", "Role": ["Tank", "DPS"]}},
                "Cardinal": {"Fluke" : {"level": 14, "dungeon": "Underrot",
                        "Class": "Hunter", "Role": ["DPS"]},
                        "Gael" : {"level": 10, "dungeon": "Brackenhide", "Class": "Druid", "Role": ["DPS"]}},
                "Sajah": {"Sajah" : {"level": 15, "dungeon": "freehold",
                        "Class": "Druid", "Role": ["Tank, DPS"]},
                        "Aythe": {"level": 7, "dungeon": "Vortex Pinnacle", "Class": "Warlock", "Role": ["DPS"]}}
                        }

#%% Classes 
class Myth_Player:
    def __init__(self, player, char_list):
        self.player_name = player
        self.list_of_chars = char_list
        self.string_list_of_chars = [x.char_name for x in char_list]
    
    def print_character_list(self):
        '''Prints all characters for this player'''
        print(f"{self.player_name} has the following characters: \n")
        for i in self.list_of_chars:
            print(i)

    def __str__(self):
        return self.player_name #+ " has the following characters:" + str(self.string_list_of_chars)

class Wow_Char:
    def __init__(self,name, char_dict):
        self.char_name = name
        self.wow_class = char_dict["Class"]
        self.role = char_dict["Role"]
        self.key_level = char_dict["level"]
        self.dungeon = char_dict["dungeon"]
    
    def print_character_info(self):
        print("Character name: " + self.char_name + "\nClass: " + self.wow_class + "\nRole(s): " + str(self.role) + "\nKey Level: " + str(self.key_level) + "\nDungeon: " + self.dungeon + "\n")

    def __str__(self):
        return ("Character name: " + self.char_name + ", Class: " + self.wow_class) #+ "\nRole(s): " + str(self.role) + "\nKey Level: " + str(self.key_level) + "\nDungeon: " + self.dungeon + "\n")

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

# %% Instantiating Myth_Players and Wow_Char
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

# print_all_players()
# print("\n")
# print_all_characters()
# print("\n")
# Jmartz.print_character_list() # Print an ind players characters
# print(Jmartz)

#%% Matchmaking
class Group:
    def __init__(self):
        self.group_members = []
        self.tank = []
        self.healer = []
        self.dps = []
        self.full_group = False
        self.string_list_of_group_members = []

    def group_strings(self):
        self.string_list_of_group_members = [x.char_name for x in self.group_members]

    def verify_group(self):
        if self.tank is not None and self.healer is not None and len(self.dps) == 3:
            print("Group is full")
            self.full_group = True
        else:
            print("Group needs more members")
            self.full_group = False

    def get_tank(self,players_list):
        for i in players_list:
            print(f"i is: {i}")
            for x in i.list_of_chars:
                print(f"x is: {x}")
                if "Tank" in x.role:
                    self.tank.append(x.char_name)
                    self.group_members.append(x)
                    players_list.pop(players_list.index(i))
                    self.group_strings()
                    self.verify_group()
                    print("Tank found")
                    print(self.tank)
                    break
                else:
                    self.verify_group()
                    print("Tank not found")
                    return False

    def request_member(self, players_list):
        if not self.tank:
            self.get_tank(players_list)
        for i in players_list:
            for x in i:
                self.check_if_role(x)

                for i in players_list:
                    print(f"i is: {i}")
                    for x in i.list_of_chars:
                        print(f"x is: {x}")
                        if "DPS" in x.role:
                            self.dps.append(x.char_name)
                            self.group_members.append(x)
                            players_list.pop(players_list.index(i))
                            self.group_strings()
                            self.verify_group()
                            print("DPS found")
                        else:
                            self.verify_group()
                            print("DPS not found")
            if not self.tank:
                for i in players_list:
                    print(f"i is: {i}")
                    for x in i.list_of_chars:
                        print(f"x is: {x}")
                        if "Tank" in x.role:
                            self.tank.append(x.char_name)
                            self.group_members.append(x)
                            players_list.pop(players_list.index(i))
                            self.group_strings()
                            self.verify_group()
                            print("Tank found")
                            print(self.tank)
                            break
                        else:
                            self.verify_group()
                            print("Tank not found")   
            if not self.healer:
                for i in players_list:
                    print(f"i is: {i}")
                    for x in i.list_of_chars:
                        print(f"x is: {x}")
                        if "Healer" in x.role:
                            self.healer.append(x.char_name)
                            self.group_members.append(x)
                            players_list.pop(players_list.index(i))
                            self.group_strings()
                            self.verify_group()
                            print("Healer found")
                            break
                        else:
                            self.verify_group()
                            print("Healer not found")
            if len(self.dps) <3:
                for i in players_list:
                    print(f"i is: {i}")
                    for x in i.list_of_chars:
                        print(f"x is: {x}")
                        if "DPS" in x.role:
                            self.dps.append(x.char_name)
                            self.group_members.append(x)
                            players_list.pop(players_list.index(i))
                            self.group_strings()
                            self.verify_group()
                            print("DPS found")
                        else:
                            self.verify_group()
                            print("DPS not found")
        print(f"group members: {self.string_list_of_group_members}")
            
    def check_if_role(self, character):
        if "Tank" in character.role:
            self.tank.append(character)
        elif "Healer" in character.role:
            self.healer.append(character)
        elif "DPS" in character.role:
            self.dps.append(character)
        else: print(f"Role not specified for {character.char_name}")

    def add_group_member(self, character):
        self.group_members.append(character)
        Group.verify_group()

    def __str__(self):
        return str(self.string_list_of_group_members)

# Test
print("before groups")
print_all_players()
print("---")
g1 = Group()
print("requesting new members...")
g1.request_member(players_list)
print("group 1 after memeber1 added:")
print(g1)
print("player list after Group member request 1")
print_all_players()
print("---")
print("g1 dps list length")
print(len(g1.dps))
if len(g1.dps) < 3:
    print("less than 3 dps")

print("requesting new member2...")
g1.request_member(players_list)
print("g1 dps list:")
print(g1.dps)
print("group 1 member list after request2:")
print(g1)
# print("After Group")
# print_all_players()
# %%
