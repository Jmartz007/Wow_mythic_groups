

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
        return self.player_name
    
    def __repr__(self) -> str:
        return "Player: " + self.player_name

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
    
    def __repr__(self) -> str:
        return "Character name: " + self.char_name + str(self.role)

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
class Pools:

    def __init__(self, playersList):
        self.playersList = playersList
        self.tankPool = []
        self.healerPool = []
        self.dpsPool = []
    

    def tank_pool(self):
        print("Generating Updated Tank pool ... ...")
        tanksPool = []
        for i in self.playersList:
            # print(f"i is: {i}")
            for x in i.list_of_chars:
                # print(f"x is: {x}")
                if "Tank" in x.role:
                    tanksPool.append(x)
                    print(f"added {x.char_name} to Tank Pool")
        print(tanksPool)
        print("Tank pool updated.\n")
        self.tankPool = tanksPool
        # return tanksPool


    def healer_pool(self):
        print("Generating Updated Healer pool ... ...")
        healersPool = []
        for i in self.playersList:
            # print(f"i is: {i}")
            for x in i.list_of_chars:
                # print(f"x is: {x}")
                if "Healer" in x.role:
                    healersPool.append(x)
                    print(f"added {x.char_name} to Healer Pool")
        print(healersPool)
        print("Healer pool Updated.\n")
        self.healerPool = healersPool
        # return healersPool


    def dps_pool(self):
        print("Generating Updated DPS pool ... ...")
        dpsPool = []
        for i in self.playersList:
            # print(f"i is: {i}")
            for x in i.list_of_chars:
                # print(f"x is: {x}")
                if "DPS" in x.role:
                    dpsPool.append(x)
                    print(f"added {x.char_name} to DPS Pool")
        print(dpsPool)
        print("DPS pool updated\n")
        self.dpsPool = dpsPool
        # return dpsPool

    def max_groups(self):
        '''This function needs to reduce the number of max tanks if one player has multiple tanks but cant tank more than one group at a time'''
        self.maxGroups = int(len(self.playersList) / 5)
        if len(self.tankPool) < self.maxGroups:
            self.maxTanks = len(self.tankPool)
        else:
            self.maxTanks = self.maxGroups
        if len(self.healerPool) < self.maxGroups:
            self.maxHealers = len(self.healerPool)
        else:
            self.maxHealers = self.maxGroups
        self.maxDps = len(self.dpsPool)

        if (self.maxTanks < self.maxHealers) and (self.maxHealers > self.maxGroups) and (self.maxTanks < self.maxGroups):
            self.maxGroups = self.maxTanks
        elif (self.maxHealers < self.maxGroups):
            self.maxGroups = self.maxHealers
        elif (self.maxDps/3 < self.maxGroups):
            self.maxGroups = self.maxDps//3
        print(f"\nMax groups: {self.maxGroups}\nMax Tanks: {self.maxTanks}\nMax_healers: {self.maxHealers}\nMax DPS: {self.maxDps}")
        return self.maxGroups, self.maxTanks, self.maxHealers, self.maxDps


class Group:
    def __init__(self, number):
        self.group_number = str(number)
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
        elif len(self.tank) < 1:
            print("Group needs a tank")
            self.full_group = False
        elif len(self.healer) < 1:
            print("Group needs a healer")
            self.full_group = False
        elif len(self.dps) < 3:
            print(f"Group needs {3-len(self.dps)} more DPS")
            self.full_group = False
        else:
            print("Group needs more members")
            self.full_group = False
            
    def __str__(self):
        return self.group_number
    
    def __repr__(self) -> str:
        return "Group number " + self.group_number + " with members: " + str(self.group_members)

class AddMembers:
    '''All get methods need to be fixed to account for modifying the list that they are iterating over. potentially using WHILE and Pools.tankPool[0].pop()
    '''
    @staticmethod
    def get_tanks(Pools):
        tanksAvail = Pools.maxGroups
        groupsList = []
        number = 1
        for tank in Pools.tankPool:
            if tanksAvail > 0:
                print(f"Tank is: {tank}")
                g = Group(number)
                print(f"New group created {g}")
                g.tank.append(tank)
                g.group_members.append(tank)
                print(f"Added tank {tank} to group")
                for player in Pools.playersList:
                    if tank in player.list_of_chars:
                        print(f"Removing {player} from player list")
                        Pools.playersList.remove(player)
                        Pools.healer_pool()
                        Pools.dps_pool()
                        break
                # g.group_strings()
                print(f"Tank added to group {g}")
                g.verify_group()
                groupsList.append(g)
                tanksAvail -= 1
                number += 1
        return groupsList
    
    @staticmethod
    def get_healer(Pools, groupsList):
        healsAvail = Pools.maxGroups
        number = 0
        for healer in Pools.healerPool:
            if healsAvail > 0:
                print(f"Healer is: {healer}")
                groupsList[number].healer.append(healer)
                groupsList[number].group_members.append(healer)
                print(f"Added {healer} to group {groupsList[number]}")
                for player in Pools.playersList:
                    if healer in player.list_of_chars:
                        print(f"Removing {player} from player list")
                        Pools.playersList.remove(player)
                        Pools.healer_pool()
                        Pools.dps_pool()
                        break
                print(f"Healer added to group {groupsList[number]}")
                groupsList[number].verify_group()
                healsAvail -= 1
                number += 1
                
    @staticmethod
    def get_dps(Pools, groupsList):
        dpsAvail = Pools.maxGroups * 3
        number = 0
        dpsNum = 0
        for dps in Pools.dpsPool:
            if dpsAvail > 0:
                print(f"DPS is: {dps}")
                groupsList[number].dps.append(dps)
                groupsList[number].group_members.append(dps)
                print(f"Added {dps} to group {groupsList[number]}")
                for player in Pools.playersList:
                    if dps in player.list_of_chars:
                        print(f"Removing {player} from player list")
                        Pools.playersList.remove(player)
                        Pools.healer_pool()
                        Pools.dps_pool()
                        break
                print(f"DPS added to group {groupsList[number]}")
                groupsList[number].verify_group()
                dpsAvail -= 1
                dpsNum += 1
                if dpsNum == 3:
                    number += 1
                    dpsNum = 0
    




if __name__ == "__main__":
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

    print("\n")
    # groupsList = AddMembers.get_tanks(players_list, tanks, max_t)
    groupsList = AddMembers.get_tanks(p)
    print("\n")
    print(players_list)
    print(len(players_list))
    # AddMembers.get_healer(players_list, groupsList, healers, max_h)
    AddMembers.get_healer(p, groupsList)
    print(players_list)
    print(len(players_list))

    AddMembers.get_dps(p, groupsList)
    print(groupsList)
    