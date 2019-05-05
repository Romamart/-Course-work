from abc import ABCMeta, abstractmethod


class BlockReward:
    __metaclass__ = ABCMeta

    @abstractmethod
    def computeBlockReward(self, height, timeToCreate):
        pass

    @abstractmethod
    def reset(self):
        pass
