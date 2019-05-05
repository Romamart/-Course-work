from src.main.blockchain.Block import Block
from src.main.miners import BaseMiner
from src.main.blockchain.NetworkStatistics import NetworkStatistics


class CompliantMiner(BaseMiner.BaseMiner):

    def __init__(self, id, hashRate, connectivity):
        super(CompliantMiner, self).__init__(id, hashRate, connectivity)

    def currentlyMiningAt(self):
        return self.__currentHead

    def currentHead(self):
        return self.__currentHead

    def blockMined(self, block, isMinerMe):
        if isMinerMe:
            if block.getHeight() > self.__currentHead.getHeight():
                self.__currentHead = block

        else:
            if self.__currentHead is None:
                self.__currentHead = block
            elif (block is not None) and (block.getHeight() > self.__currentHead.getHeight()):
                self.__currentHead = block

    def initialize(self, genesis, networkStatistic):
        self.__currentHead = genesis

    def networkUpdate(self, statistics):
        pass
