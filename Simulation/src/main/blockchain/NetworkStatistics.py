class NetworkStatistics:

    def __init__(self, orphanRate, totalHashRate, totalConnectivity):
        self.__orphanRate = orphanRate
        self.__totalHashRate = totalHashRate
        self.__totalConnectivity = totalConnectivity

    def getOrphanRate(self):
        return self.__orphanRate

    def getTotalConnectivity(self):
        return self.__totalConnectivity

    def getTotalHashRate(self):
        return self.__totalHashRate
