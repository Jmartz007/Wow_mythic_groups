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
    def __init__(self,name, playerName, char_dict):
        self.playerName = playerName
        self.char_name = name
        self.wow_class = char_dict["Class"]
        self.role = char_dict["Role"]
        self.hConf = char_dict.get("Healer Skill")
        self.tConf = char_dict.get("Tank Skill")
        self.dpsConf = char_dict.get("DPS Skill")
        self.key_level = char_dict["Key Level"]
        self.dungeon = char_dict["Dungeon"]
    
    def print_character_info(self):
        print("Character name: " + self.char_name + "\nClass: " + self.wow_class + "\nRole(s): " + str(self.role) + "\nKey Level: " + str(self.key_level) + "\nDungeon: " + self.dungeon + "\n")

    def __str__(self):
        return f"Character: {self.char_name}, {self.wow_class} - {self.key_level}, {self.dungeon} "
        # return ("Character name: " + self.char_name + ", Class: " + self.wow_class)
    
    def __repr__(self) -> str:
        return "Character name: " + self.char_name + str(self.role) + " Owned by: " + self.playerName

### Printing Helper Functions
def print_all_players(players_list):
    # Prints all players signed up
    print("List of all players: ")
    for i in range(len(players_list)):
        print(players_list[i])

def print_all_characters():
    # Prints all characters from all players in the pool
    print("List of all characters and keys: ")
    for i in players_list:
        for x in i.list_of_chars:
            print(x)

###  Instantiating Myth_Players and Wow_Char
def players_gen(keystone_dict:dict) -> list[Myth_Player]:
    # print("Generating player objects and character objects ...  ...")
    logger.info("Generating player objects and character objects ...  ...")
    players_list = []
    for i in keystone_dict:
        char_list = list(keystone_dict[i].keys())
        # print(i) ## Player names ie: Jmartz
        # print(char_list) ## Character names ie: Calioma
        toon_list = []
        for num in char_list:
            locals()[num] = Wow_Char(num, i, keystone_dict[i][num])  # create an instance of the character object
            toon_list.append(locals()[num])
        locals()[i] = Myth_Player(i, toon_list)  # Create an instance of the player object with the list of character objects
        players_list.append(locals()[i])
    return players_list



### Player Pools
class Pools:

    def __init__(self, playersList):
        self.playersList = playersList
        self.tankPool = []
        self.healerPool = []
        self.dpsPool = []
        self.maxGroups = int(len(self.playersList) / 5)



    def tank_pool(self):
        logger.info("Generating Updated Tank pool ... ...")
        tanksPool = []
        for i in self.playersList:
            # print(f"i is: {i}")
            for x in i.list_of_chars:
                # print(f"x is: {x}")
                if "Tank" in x.role:
                    tanksPool.append(x)
                    # print(f"added {x.char_name} to Tank Pool")


        tanksPool.sort(key=lambda p: self.Tcompetency_sorting(p), reverse=True)
        tanksPool.sort(key=lambda p: ( self.playercountSorting(p), self.roleSorting(p) ))
        
        logger.debug(f"\n[][][][][] Tank pool updated. There are now {len(tanksPool)} players in the tank pool.\n")
        self.tankPool = tanksPool


    def healer_pool(self):
        # logger.info("Generating Updated Healer pool ... ...")
        healersPool = []
        for i in self.playersList:
            # print(f"i is: {i}")
            for x in i.list_of_chars:
                # print(f"x is: {x}")
                if "Healer" in x.role:
                    healersPool.append(x)
                    # print(f"added {x.char_name} to Healer Pool")
        
        

        
        healersPool.sort(key=lambda p: (self.playercountSorting(p), self.roleSorting(p) ))
        sorted(healersPool, key=lambda p: self.Hcompetency_sorting(p), reverse=True)
        # logger.debug(f"\n+++++ Healer pool updated. There are now {len(healersPool)} players in the healer pool.\n")

        self.healerPool = healersPool
        # return healersPool


    def dps_pool(self):
        # logger.info("Generating Updated DPS pool ... ...")
        deepsPool = []
        for i in self.playersList:
            # print(f"i is: {i}")
            for x in i.list_of_chars:
                # print(f"x is: {x}")
                if "DPS" in x.role:
                    deepsPool.append(x)
                    # print(f"added {x.char_name} to DPS Pool")
        # print(deepsPool)
        # logger.debug(f"\n----- DPS pool updated. There are now {len(deepsPool)} players in the DPS pool.\n")
        self.dpsPool = deepsPool
        # return dpsPool


    ### Sorting functions to be used in order to apply some kind of priority in group making. These functions should apply at the player pool level

    # This sorting function will give priority to those with fewer number of characters (1 character > 3 characters)
    def playercountSorting(self, rolePool):
        count = 0
        for player in self.playersList:
            # print(player)
            # print("player -------------")
            for char in  player.list_of_chars:
                # print("char.char_name")
                # print(char.playerName)
                # print("p.char_name")
                # print(rolePool.playerName)
                if rolePool.playerName == char.playerName:
                    # print("adding 1 to count")
                    count += 1
        # print(f"final count: {count}")
        return count

    #this sorting function will give priority to characters with fewer roles (1 role > 3 roles)
    def roleSorting(self, rolePool):
        return len((rolePool.role))
    

    def Hcompetency_sorting(self, rolePool):
        return rolePool.hConf
    
    def Tcompetency_sorting(self, rolePool):
        return rolePool.tConf




    def max_groups(self):
        # This function needs to reduce the number of max tanks if one player has multiple tanks but cant tank more than one group at a time
        
        pList = []
        for t in self.tankPool:
            if t.playerName not in pList:
                pList.append(t.playerName)
        if len(pList) < self.maxGroups:
            self.maxTanks = len(pList)
        else:
            self.maxTanks = self.maxGroups

        hList = []
        for h in self.healerPool:
            if h.playerName not in hList:
                hList.append(h.playerName)
        if len(hList) < self.maxGroups:
            self.maxHealers = len(hList)
            if self.maxTanks > self.maxHealers:
                self.maxTanks = self.maxHealers
        else:
            self.maxHealers = self.maxGroups

        self.maxDps = len(self.dpsPool)

        if (self.maxTanks < self.maxHealers) and (self.maxHealers >= self.maxGroups) and (self.maxTanks < self.maxGroups):
            self.maxGroupsFinal = self.maxTanks
        elif (self.maxHealers < self.maxGroups):
            self.maxGroupsFinal = self.maxHealers
        elif (self.maxDps/3 < self.maxGroups):
            self.maxGroupsFinal = self.maxDps//3
        else:
            self.maxGroupsFinal = self.maxGroups

        
        logger.info(f"\nMax groups: {self.maxGroupsFinal}\nMax Tanks: {self.maxTanks}\nMax healers: {self.maxHealers}\nMax DPS: {self.maxDps}")
        return self.maxGroupsFinal, self.maxTanks, self.maxHealers, self.maxDps


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
        if self.tank and self.healer and len(self.dps) == 3:
            logger.info("Group is full")
            # print("Group is full")
            self.full_group = True
        elif len(self.tank) < 1:
            # logger.debug("Group needs a tank")
            self.full_group = False
        elif len(self.healer) < 1:
            # logger.debug("Group needs a healer")
            self.full_group = False
        elif len(self.dps) < 3:
            # logger.debug(f"Group needs {3-len(self.dps)} more DPS")
            self.full_group = False
        else:
            # logger.debug("Group needs more members")
            self.full_group = False
        duplicates = [x.playerName for x in self.group_members if self.group_members.count(x.playerName) > 1]
        # logger.debug(f"Duplicate players found: {duplicates}")
            
    def __str__(self):
        return "Group number " + self.group_number + " with members: " + str(self.group_members)
    
    def __repr__(self) -> str:
        return "Group number " + self.group_number + " with members: " + str(self.group_members)

class AddMembers:

    @staticmethod
    def get_tanks(Pools):
        tanksAvail = Pools.maxGroupsFinal
        groupsList = []
        removedList = []
        number = 1
        for tank in Pools.tankPool:
            if tanksAvail > 0 and (tank.playerName not in [x.playerName for x in removedList]):
                logger.debug(f"Tank is: {tank}")
                g = Group(number)
                logger.debug(f"New group created {g}")
                g.tank.append(tank)
                g.group_members.append(tank)
                logger.debug(f"Added tank {tank} to group")
                for player in Pools.playersList:
                    if tank in player.list_of_chars:
                        # logger.debug(f"Removing {player} from player list")
                        for char in player.list_of_chars:
                            removedList.append(char)
                        Pools.playersList.remove(player)
                        Pools.tank_pool()
                        Pools.healer_pool()
                        Pools.dps_pool()
                        break
                # print(f"Tank added to group {g}")
                # logger.debug(f"Tank added to group {g}")
                g.verify_group()
                groupsList.append(g)
                tanksAvail -= 1
                number += 1
        return groupsList
    
    @staticmethod
    def get_healer(Pools, groupsList):
        healsAvail = Pools.maxGroupsFinal
        number = 0
        removedList = []
        try:
            for healer in Pools.healerPool:
                if healsAvail > 0 and (healer.playerName not in [x.playerName for x in removedList]):
                    logger.debug(f"Adding {healer} to group {groupsList[number]}")
                    groupsList[number].healer.append(healer)
                    groupsList[number].group_members.append(healer)
                    for player in Pools.playersList:
                        if healer in player.list_of_chars:
                            # logger.debug(f"Removing {player} from player list")
                            for char in player.list_of_chars:
                                removedList.append(char)
                            Pools.playersList.remove(player)
                            Pools.healer_pool()
                            Pools.dps_pool()
                            break
                    logger.debug(f"Healer added to group {groupsList[number]}")
                    groupsList[number].verify_group()
                    healsAvail -= 1
                    number += 1
        except IndexError as error:
            logger.exception(f"An exception occurred: {error} ")

                
    @staticmethod
    def get_dps(Pools, groupsList):
        dpsAvail = Pools.maxGroupsFinal * 3
        number = 0
        dpsNum = 0
        removedList = []
        try:
            for dps in Pools.dpsPool:
                if dpsAvail > 0 and (dps.playerName not in [x.playerName for x in removedList]):
                    # print(f"DPS is: {dps}")
                    # logger.debug(f"Adding {dps} to group {groupsList[number]}")
                    groupsList[number].dps.append(dps)
                    groupsList[number].group_members.append(dps)
                    dpsNum += 1
                    for player in Pools.playersList:
                        if dps in player.list_of_chars:
                            # logger.debug(f"Removing {player} from player list")
                            for char in player.list_of_chars:
                                removedList.append(char)
                            Pools.playersList.remove(player)
                            Pools.healer_pool()
                            Pools.dps_pool()
                            break
                    # logger.debug(f"DPS added to group {groupsList[number]}")
                    groupsList[number].verify_group()
                    dpsAvail -= 1

                if dpsNum == 3:
                    number += 1
                    dpsNum = 0
        except IndexError as error:
            logger.exception(f"an error ocurred: {error}")
    




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

    # groupsList = AddMembers.get_tanks(players_list, tanks, max_t)
    groupsList = AddMembers.get_tanks(p)
    # AddMembers.get_healer(players_list, groupsList, healers, max_h)
    AddMembers.get_healer(p, groupsList)
    AddMembers.get_dps(p, groupsList)
    logger.info(f"number of players left {len(players_list)}:")
    logger.info(players_list)
    logger.info(p.max_groups)
    logger.info(f"Number of groups formed: {len(groupsList)}")
    logger.info(groupsList)
    