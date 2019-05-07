from src.main.blockchain.SimulationRandom import SimulationRandom
from src.main.blockchain.Block import Block
from src.main.miners.BaseMiner import BaseMiner
from src.main.blockchain.NetworkStatistics import NetworkStatistics
import logging
import operator


class BitcoinNetwork:
    __forkStart = -1

    def __init__(self, blockReward, churnFunction, churnProbability, orphanRate):
        self.__blockReward = blockReward
        self.__churnProbability = churnProbability
        self.__churnFunction = churnFunction
        self.__orphanRate = orphanRate
        self.__broadcastRNG = SimulationRandom()

    @staticmethod
    def __merge(dict1, dict2):
        b1 = list(dict1.keys())
        b2 = list(dict2.keys())
        for i in b2:
            if i in b1:
                dict2[i] = dict1[i] + dict2[i]
        dict1.update(dict2)
        return dict1

    def simulation(self, numBlocks, miners, miningRNG):
        forkStart = -1
        genesis = Block(None, "Satoshi", 0)
        totalConnectivity = 0
        totalHashRate = 0
        for miner in miners:
            connectivity = miner.getConnectivity()
            totalConnectivity += connectivity
            hashRate = miner.getHashRate()
            totalHashRate += hashRate

        statistics = NetworkStatistics(self.__orphanRate, totalHashRate, totalConnectivity)

        for miner in miners:
            miner.initialize(genesis, statistics)
        singleOrphanRate = self.__orphanRate / (self.__orphanRate + 1)
        for i in range(numBlocks):

            if miningRNG.random() < self.__churnProbability:
                networkStatistics = self.__churnFunction.churnNetwork(self, self.__orphanRate, miners)
                # for m in miners:
                #     m.networkUpdate(networkStatistics)

            # for m in miners:
            #     print(m)
            winnningMiners = {}
            for m in miners:
                minerDoubleSimpleEntry = {m: miningRNG.sampleExponential(m.getHashRate())}
                winnningMiners.update(minerDoubleSimpleEntry)
            winnningMiners = list(sorted(winnningMiners.items(), key=operator.itemgetter(1)))


            for j in range(len(winnningMiners)):
                winnningMiners[j] = dict([winnningMiners[j]])
            initialMessages = dict()
            currentOrphanProbability = singleOrphanRate
            minedRewards = dict()
            for winner in winnningMiners:
                winningMiner = list(winner.keys())[0]
                previousBlock = winningMiner.currentlyMiningAt()
                reward = self.__blockReward.computeBlockReward(self, previousBlock.getHeight() + 1,
                                                               winner[winningMiner])
                nextBlock = Block(previousBlock, winningMiner.getId(), reward)
                blockMassage = self.__BlockMassage(nextBlock, winningMiner)
                minedRewards = self.__merge(minedRewards, {winningMiner: reward})
                initialMessages.update({blockMassage: 0.})
                k = miningRNG.random()
                if k < currentOrphanProbability:
                    currentOrphanProbability *= singleOrphanRate
                else:
                    break
            self.__propagateBlock(initialMessages, miners)

        totalRewards = 0
        for doub in minedRewards.values():
            doubleValue = float(doub)
            totalRewards += doubleValue
        logging.debug("Simulation finished with block mining distribution {0}".format(minedRewards))
        k = {miner: miner.currentHead().getHeight() for miner in miners}
        return max(k, key=k.get).currentHead()

    def __propagateBlock(self, initialMessages, miners):
        deliveredMessages = []

        messageQueue = initialMessages
        minHeight = 0

        while initialMessages:
            # print(initialMessages)
            # message = min(messageQueue.items(), key=operator.itemgetter(1))[0]
            message = min(messageQueue, key=messageQueue.get)
            # print(message)
            message.deliver()
            deliveredMessages.append(message)
            currentTime = messageQueue.pop(message)
            sender = message.getRecipient()
            broadcastBlock = sender.currentHead()
            if (broadcastBlock.getHeight() >= minHeight):
                minHeight = max(broadcastBlock.getHeight(), minHeight)
                for m in miners:
                    blockMessage = self.__BlockMassage(broadcastBlock, m)
                    if not deliveredMessages.__contains__(blockMessage):
                        messageQueue.update({blockMessage: currentTime + self.__broadcastRNG
                                            .sampleExponential(blockMessage.getRecipient().getConnectivity()
                                                               * sender.getConnectivity())})

    def __printForks(self, miners):
        forks = {}
        for miner in miners:
            forks = self.__merge(forks, {miner.currentHead(): miner.getHashRate()})
        if (len(forks) > 1) and (self.__forkStart):
            seen = False
            best = 0
            for block in list(forks.keys()):
                height = block.getHeight()
                if (not seen) or (height > best):
                    seen = True
                    best = height
            self.__forkStart = -1

    class __BlockMassage:

        def __init__(self, block, recipient):
            self.__block = block
            self.__recipient = recipient

        def deliver(self):
            if self.__block.getMinedBy() == (self.__recipient.getId()):
                if self.__block.getHeight() >= self.__recipient.currentlyMiningAt().getHeight():
                    self.__recipient.blockMined(self.__block, True)

            else:
                self.__recipient.blockMined(self.__block, False)

        def __eq__(self, other):
            otherMassage = other
            return (self.__block == otherMassage.__block) and (self.__recipient == otherMassage.__recipient)

        def __hash__(self):
            return object.__hash__(self.__block)

        def getRecipient(self):
            return self.__recipient
