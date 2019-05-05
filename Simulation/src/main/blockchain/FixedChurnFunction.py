from src.main.blockchain.ChurnFunction import ChurnFunction
from src.main.blockchain.NetworkStatistics import NetworkStatistics


class FixedChurnFunction(ChurnFunction):

    def churnNetwork(self,orphanRate, miners):
        totalHashRate = 0
        for miner in miners:
            hashRate = miner.getHashRate()
        totalHashRate += hashRate
        totalConnectivity = 0
        for miner in miners:
            connectivity = miner.getConnectivity()
        totalConnectivity += connectivity

        return NetworkStatistics(orphanRate, totalHashRate, totalConnectivity)