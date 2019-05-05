
class Block:

    def __init__(self, previousBlock, mineBy, blockValue):
        self.__previousBlock = previousBlock
        self.__height = 0 if previousBlock is None else previousBlock.__height + 1
        self.__mineBy = mineBy
        self.__blockValue = blockValue

    def getPreviousBlock(self):
        return self.__previousBlock

    def getHeight(self):
        return self.__height

    def getBlockValue(self):
        return self.__blockValue

    def getMinedBy(self):
        return self.__mineBy

    def __str__(self):
        return 'Block[height={0},blockValue={1},minedBy={2}]'.format(self.__height, self.__blockValue, self.__mineBy)
