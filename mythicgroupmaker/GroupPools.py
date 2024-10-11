"""This module is responsible for creating the class pools"""

import logging

from .MythPlayer import Myth_Player


logger = logging.getLogger(f"main.{__name__}")


### Player Pools
class Pools:
    """This class generates role based pools from a list of Myth_Player objects. Each pool method contains its own sorting for priority"""

    def __init__(self, MythPlayerList: list[Myth_Player]):
        self.playersList = MythPlayerList
        self.tankPool = []
        self.healerPool = []
        self.dpsPool = []
        self.maxGroups = int(len(self.playersList) / 5)
        self.tank_pool()
        self.healer_pool()
        self.dps_pool()
        self.max_groups()

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
        tanksPool.sort(key=lambda p: (self.playercountSorting(p), self.roleSorting(p)))

        logger.debug(
            f"\n[][][][][] Tank pool updated. There are now {len(tanksPool)} players in the tank pool.\n"
        )
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

        healersPool.sort(
            key=lambda p: (self.playercountSorting(p), self.roleSorting(p))
        )
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
            for char in player.list_of_chars:
                # print("char.char_name")
                # print(char.playerName)
                # print("p.char_name")
                # print(rolePool.playerName)
                if rolePool.playerName == char.playerName:
                    # print("adding 1 to count")
                    count += 1
        # print(f"final count: {count}")
        return count

    # this sorting function will give priority to characters with fewer roles (1 role > 3 roles)
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

        if (
            (self.maxTanks < self.maxHealers)
            and (self.maxHealers >= self.maxGroups)
            and (self.maxTanks < self.maxGroups)
        ):
            self.maxGroupsFinal = self.maxTanks
        elif self.maxHealers < self.maxGroups:
            self.maxGroupsFinal = self.maxHealers
        elif self.maxDps / 3 < self.maxGroups:
            self.maxGroupsFinal = self.maxDps // 3
        else:
            self.maxGroupsFinal = self.maxGroups

        logger.info(
            f"\nMax groups: {self.maxGroupsFinal}\nMax Tanks: {self.maxTanks}\nMax healers: {self.maxHealers}\nMax DPS: {self.maxDps}"
        )
        return self.maxGroupsFinal, self.maxTanks, self.maxHealers, self.maxDps


class Group:
    """This class defines the group and the members it contains. This is where the Wow_Char objects are ultimately sorted into."""

    def __init__(self, number):
        self.group_number = str(number)
        self.group_members = []
        self.tank = []
        self.healer = []
        self.dps = []
        self.full_group = False
        self.string_list_of_group_members = []

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
        duplicates = [
            x.playerName
            for x in self.group_members
            if self.group_members.count(x.playerName) > 1
        ]
        # logger.debug(f"Duplicate players found: {duplicates}")

    def get_tanks(self):
        tanksAvail = self.maxGroupsFinal
        groupsList = []
        removedList = []
        number = 1
        for tank in self.tankPool:
            if tanksAvail > 0 and (
                tank.playerName not in [x.playerName for x in removedList]
            ):
                logger.debug(f"Tank is: {tank}")
                g = Group(number)
                logger.debug(f"New group created {g}")
                g.tank.append(tank)
                g.group_members.append(tank)
                logger.debug(f"Added tank {tank} to group")
                for player in self.playersList:
                    if tank in player.list_of_chars:
                        # logger.debug(f"Removing {player} from player list")
                        for char in player.list_of_chars:
                            removedList.append(char)
                        self.playersList.remove(player)
                        self.tank_pool()
                        self.healer_pool()
                        self.dps_pool()
                        break
                # print(f"Tank added to group {g}")
                # logger.debug(f"Tank added to group {g}")
                g.verify_group()
                groupsList.append(g)
                tanksAvail -= 1
                number += 1
        return groupsList

    def get_healer(Pools, groupsList):
        healsAvail = Pools.maxGroupsFinal
        number = 0
        removedList = []
        try:
            for healer in Pools.healerPool:
                if healsAvail > 0 and (
                    healer.playerName not in [x.playerName for x in removedList]
                ):
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

    def get_dps(Pools, groupsList):
        dpsAvail = Pools.maxGroupsFinal * 3
        number = 0
        dpsNum = 0
        removedList = []
        try:
            for dps in Pools.dpsPool:
                if dpsAvail > 0 and (
                    dps.playerName not in [x.playerName for x in removedList]
                ):
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

    def print_group(self):
        self.string_list_of_group_members = [x.char_name for x in self.group_members]

    def __str__(self):
        return (
            "Group number "
            + self.group_number
            + " with members: "
            + str(self.group_members)
        )

    def __repr__(self) -> str:
        return (
            "Group number "
            + self.group_number
            + " with members: "
            + str(self.group_members)
        )


class AddMembers:

    @staticmethod
    def get_tanks(Pools):
        tanksAvail = Pools.maxGroupsFinal
        groupsList = []
        removedList = []
        number = 1
        for tank in Pools.tankPool:
            if tanksAvail > 0 and (
                tank.playerName not in [x.playerName for x in removedList]
            ):
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
                if healsAvail > 0 and (
                    healer.playerName not in [x.playerName for x in removedList]
                ):
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
                if dpsAvail > 0 and (
                    dps.playerName not in [x.playerName for x in removedList]
                ):
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
