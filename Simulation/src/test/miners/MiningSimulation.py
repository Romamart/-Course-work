from src.main.blockchain.BitcoinNetwork import BitcoinNetwork
from src.main.blockchain.FixedChurnFunction import FixedChurnFunction
from src.main.blockchain.FixedReward import FixedReward
from src.main.blockchain.SimulationRandom import SimulationRandom
from src.main.miners.CompliantMiner import CompliantMiner
from src.main.blockchain.NormalChurnFunction import NormalChurnFunction
from src.main.blockchain.LognormalReward import LognormalReward
from src.main.blockchain.BlockReward import BlockReward
import logging


class MiningSimulation:
    def __init__(self):
        self.__LOGGER = logging.getLogger()

    @staticmethod
    def __merge(dict1, dict2):
        b1 = list(dict1.keys())
        b2 = list(dict2.keys())
        for i in b1:
            if i in b2:
                dict2[i] = dict1[i] + dict2[i]
        dict1.update(dict2)
        return dict1

    def simulateDifferentNetworkPower(self):
        miner1 = CompliantMiner("Miner1", 51, 1)
        miner2 = CompliantMiner("Miner2", 15, 1)
        miner3 = CompliantMiner("Miner3", 14, 1)
        miner4 = CompliantMiner("Miner4", 10, 1)
        miner5 = CompliantMiner("Miner5", 5, 1)
        miner6 = CompliantMiner("Miner6", 5, 1)
        miners = [miner1, miner2, miner3, miner4, miner5, miner6]

        self.__runSimulation(miners, FixedReward, FixedChurnFunction)

    def __runSimulation(self, miners, rewardFunction, churnFunction):
        print("Hello")
        for m in miners:
            print(str(m))
        print(type(miners))
        numIterations = 120
        networkController = BitcoinNetwork(rewardFunction, churnFunction, 0.005, 0.02)

        profits = dict()

        rng = SimulationRandom(2345)

        for i in range(numIterations):
            numBlocks = int(rng.sampleExponentialRandom(0.0001))
            rewardFunction.reset(self)
            head = networkController.simulation(numBlocks, miners, rng)
            current = head

            while current is not None:
                winningMiner = current.getMinedBy()
                profits = self.__merge(profits, {winningMiner: current.getBlockValue()})
                current = current.getPreviousBlock()

        relativeProfits = dict()
        totalProfits = sum(profits.values())
        for winingMiner in profits:
            profit = profits[winingMiner]
            relativeProfit = profit / totalProfits
            # logging.info("{0} has made {1}% of the profits".format(winingMiner, 100. * relativeProfit))
            print("{0} has made {1}% of the profits".format(winingMiner, 100. * relativeProfit))
            relativeProfits.update({winingMiner: relativeProfit})
        return relativeProfits


# if __name__ == '__main__':
#     MiningSimulation.simulateDifferentNetworkPower(self)

Test = MiningSimulation()
Test.simulateDifferentNetworkPower()
