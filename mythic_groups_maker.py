

### Data
keystone_dict = {
                "Jmartz": {"Calioma" : {"Level": 7, "Dungeon": "freehold", "Class": "Priest", "Role": ["Healer"]},
                        "Solemartz": {"Level": 3, "Dungeon": "Vortex Pinnacle", "Class": "Mage", "Role": ["DPS"]},
                        "Jmartz": {"Level": 16, "Dungeon": "Halls of Infusion", "Class": "Warrior", "Role": ["Tank", "DPS"]}},
                "Cardinal": {"Fluke" : {"Level": 14, "Dungeon": "Underrot", "Class": "Hunter", "Role": ["DPS"]},
                        "Gael" : {"Level": 10, "Dungeon": "Brackenhide", "Class": "Druid", "Role": ["DPS"]}},
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
        self.key_level = char_dict["Level"]
        self.dungeon = char_dict["Dungeon"]
    
    def print_character_info(self):
        print("Character name: " + self.char_name + "\nClass: " + self.wow_class + "\nRole(s): " + str(self.role) + "\nKey Level: " + str(self.key_level) + "\nDungeon: " + self.dungeon + "\n")

    def __str__(self):
        return ("Character name: " + self.char_name + ", Class: " + self.wow_class) #+ "\nRole(s): " + str(self.role) + "\nKey Level: " + str(self.key_level) + "\nDungeon: " + self.dungeon + "\n")

### Printing Helper Functions
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

###  Instantiating Myth_Players and Wow_Char
def players_gen(keystone_dict):
    print("Generating player objects and character objects ...  ...")
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
    print("\n")
    return players_list



### Player Pools

def healer_pool(players_list):
    print("Generating Healer pool ... ...")
    availablePlayersPool = players_list.copy()
    healersPool = []
    for i in availablePlayersPool:
        print(f"i is: {i}")
        for x in i.list_of_chars:
            print(f"x is: {x}")
            if "Healer" in x.role:
                healersPool.append(x.char_name)
                print(f"added {x.char_name} to Healer Pool")
    print(healersPool)
    print("Healer pool created\n")
    return healersPool


def tank_pool(players_list):
    print("Generating Tank pool ... ...")
    availablePlayersPool = players_list.copy()
    tanksPool = []
    for i in availablePlayersPool:
        print(f"i is: {i}")
        for x in i.list_of_chars:
            print(f"x is: {x}")
            if "Tank" in x.role:
                tanksPool.append(x.char_name)
                print(f"added {x.char_name} to Tank Pool")
    print(tanksPool)
    print("Tank pool created\n")
    return tanksPool


def dps_pool(players_list):
    print("Generating DPS pool ... ...")
    availablePlayersPool = players_list.copy()
    dpsPool = []
    for i in availablePlayersPool:
        print(f"i is: {i}")
        for x in i.list_of_chars:
            print(f"x is: {x}")
            if "DPS" in x.role:
                dpsPool.append(x.char_name)
                print(f"added {x.char_name} to DPS Pool")
    print(dpsPool)
    print("DPS pool created\n")
    return dpsPool

### Matchmaking

def max_groups(players_list, tanksPool, healersPool, dpsPool):
    max_groups = int(len(players_list) / 5)
    if len(tanksPool) < max_groups:
        max_tanks = len(tanksPool)
    else:
        max_tanks = max_groups
    if len(healersPool) < max_groups:
        max_healers = len(healersPool)
    else:
        max_healers = max_groups
    max_dps = len(dpsPool)

    if (max_tanks < max_healers) and (max_healers > max_groups) and (max_tanks < max_groups):
        max_groups = max_tanks
    elif (max_healers < max_groups):
        max_groups = max_healers
    elif (max_dps/3 < max_groups):
        max_groups = max_dps//3
    print(f"\nMax groups: {max_groups}\nMax Tanks: {max_tanks}\nMax_healers: {max_healers}\nMax DPS: {max_dps}")
    return max_groups, max_tanks, max_healers, max_dps


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
        elif self.tank < 1:
            print("Group needs a tank")
            self.full_group = False
        elif self.healer < 1:
            print("Group needs a healer")
            self.full_group = False
        elif self.dps < 3:
            print(f"Group needs {3-self.dps} more DPS")
            self.full_group = False
        else:
            print("Group needs more members")
            self.full_group = False
            
    def __str__(self):
        return str(self.string_list_of_group_members)

class AddMembers:
    '''Parameters need to be edited to accept the tanks list and the player list or character list. Then needs to be able to .pop those character objects out of the player pool
    '''
    @staticmethod
    def get_tank(group, players_list, tank_pool):
        while len(group.tank) < max_t:
            for i in tank_pool:
                print(f"i is: {i}")
                group.tank.append(i)
                group.group_members.append(i)
                players_list.pop(players_list.index(i))
                group.group_strings()
                print("Tank found")
                print(group.tank)
                group.verify_group()

if __name__ == "__main__":
    players_list = players_gen(keystone_dict)

    healers = healer_pool(players_list)
    tanks = tank_pool(players_list)
    dpsers = dps_pool(players_list)

    max_g, max_t, max_h, max_dps = max_groups(players_list)
