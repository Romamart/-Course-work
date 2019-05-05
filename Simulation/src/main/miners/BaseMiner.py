from abc import ABCMeta, abstractmethod


class BaseMiner:
    __metaclass__ = ABCMeta

    def __init__(self, id, hashRate, connectivity):
        self.__id = id
        self.__hashRate = hashRate
        self.__connectivity = connectivity

    @abstractmethod
    def getConnectivity(self):
        return self.__connectivity

    @abstractmethod
    def setConnectivity(self, connectivity):
        self.__connectivity = connectivity

    @abstractmethod
    def setHashRate(self, hashRate):
        self.__hashRate = hashRate

    @abstractmethod
    def getHashRate(self):
        return self.__hashRate

    @abstractmethod
    def getId(self):
        return self.__id

    @abstractmethod
    def __str__(self):
        return "Miner[id={0},hashRate={1},connectivity={2}]".format(self.__id, self.__hashRate, self.__connectivity)
