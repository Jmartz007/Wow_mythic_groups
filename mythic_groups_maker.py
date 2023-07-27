

#%% Data
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

### Player and Character Classes 
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
def print_all_players(players_list):
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
    print(i) ## Player names ie: Jmartz
    print(char_list) ## Character names ie: Calioma
    toon_list = []
    for num in char_list:
        locals()[num] = Wow_Char(num, keystone_dict[i][num])  # create an instance of the character object
        toon_list.append(locals()[num])
    locals()[i] = Myth_Player(i, toon_list)  # Create an instance of the player object with the list of character objects
    players_list.append(locals()[i])

# print_all_players(players_list)
# print("\n")
# print_all_characters()
# print("\n")
# Jmartz.print_character_list() # Print an ind players characters
# print(Jmartz)


### Player Pools

def healer_pool(players_list):
    availablePlayersPool = players_list.copy()
    healersPool = []
    print_all_players(availablePlayersPool)
    for i in availablePlayersPool:
        print(f"i is: {i}")
        for x in i.list_of_chars:
            print(f"x is: {x}")
            if "Healer" in x.role:
                healersPool.append(x.char_name)
                print(f"added {x.char_name} to Healer Pool")
    return healersPool
healers = healer_pool(players_list)
print(healers)

def tank_pool(players_list):
    availablePlayersPool = players_list.copy()
    tankPool = []
    print_all_players(availablePlayersPool)
    for i in availablePlayersPool:
        print(f"i is: {i}")
        for x in i.list_of_chars:
            print(f"x is: {x}")
            if "Tank" in x.role:
                tankPool.append(x.char_name)
                print(f"added {x.char_name} to Tank Pool")
    return tankPool
tanks = tank_pool(players_list)
print(tanks)

def dps_pool(players_list):
    availablePlayersPool = players_list.copy()
    dpsPool = []
    print_all_players(availablePlayersPool)
    for i in availablePlayersPool:
        print(f"i is: {i}")
        for x in i.list_of_chars:
            print(f"x is: {x}")
            if "DPS" in x.role:
                dpsPool.append(x.char_name)
                print(f"added {x.char_name} to DPS Pool")
    return dpsPool
dpsers = dps_pool(players_list)
print(dpsers)


### Matchmaking

def max_groups(players_list):
    max_groups = int(len(players_list) / 5)
    max_tanks = max_groups
    max_healers = max_groups
    max_dps = max_groups * 3
    print(f"\nMax groups: {max_groups}\nMax Tanks: {max_tanks}\nMax_healers: {max_healers}\nMax DPS: {max_dps}")
    return max_groups, max_tanks, max_healers, max_dps

max_g, max_t, max_h, max_dps = max_groups(players_list)


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

    """ def request_member(self, players_list):
        if not self.tank:
            self.get_tank(players_list)
        for i in players_list:
            for x in i.list_of_chars:
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
        print(f"group members: {self.string_list_of_group_members}") """
            
    def __str__(self):
        return str(self.string_list_of_group_members)

class AddMembers:
    '''Parameters need to be edited to accept the tanks list and the player list or character list. Then needs to be able to .pop those character objects out of the player pool
    '''
    @staticmethod
    def get_tank(self,players_list):
        while len(self.tank) < max_t:
            for i in tanks:
                print(f"i is: {i}")
                self.tank.append(i)
                self.group_members.append(i)
                players_list.pop(players_list.index(i))
                self.group_strings()
                self.verify_group()
                print("Tank found")
                print(self.tank)


### Test Functions

def test_new_group():
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
    # print("After Group")
    # print_all_players()
    # %%


