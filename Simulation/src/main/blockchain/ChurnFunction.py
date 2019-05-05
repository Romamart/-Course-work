from abc import ABCMeta, abstractmethod


class ChurnFunction:
    __metaclass__ = ABCMeta

    @abstractmethod
    def churnNetwork(self,orphanRate,miners):
        pass
