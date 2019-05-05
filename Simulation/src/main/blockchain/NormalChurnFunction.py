import math

from src.main.blockchain.ChurnFunction import ChurnFunction
from src.main.blockchain.NetworkStatistics import NetworkStatistics


class NormalChurnFunction(ChurnFunction):

    def __init__(self, hashRateSD, connectivitySD, rng):
        self.__connectivitySD = connectivitySD
        self.__hashRateSD = hashRateSD
        self.__rng = rng

    def churnNetwork(self, orphanRate, miners):
        totalHashRate = 0
        totalConnectivity = 0
        for miner in miners:
            while True:
                newConnectivity = int(round(self.__rng.sampleNormal(miner.getConnectivity(), self.__connectivitySD)))
                print(miner.getConnectivity())
                if newConnectivity < 1:
                    break
            totalConnectivity += newConnectivity
            while True:
                newHashRate = int(round(self.__rng.sampleNormal(miner.getHashRate(), self.__hashRateSD)))
                print(newHashRate)
                if (newHashRate < 1):
                    break

            totalHashRate += newHashRate

            miner.setHashRate(newHashRate)
            miner.setConnectivity(newConnectivity)
            print('yes')
        return NetworkStatistics(orphanRate, totalHashRate, totalConnectivity)
