from src.main.blockchain.BlockReward import BlockReward


class LognormalReward(BlockReward):
    __previousRewards = []

    def __init__(self, rng):
        self.__rng = rng

    def computeBlockReward(self, height, timeTocreate):
        while len(self.__previousRewards) <= height:
            self.__previousRewards.append(self.__rng.sampleLogNormal(0, 2))

        return self.__previousRewards[height - 1]

    def reset(self):
        __previousRewards = []
