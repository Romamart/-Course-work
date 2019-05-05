from src.main.blockchain.BlockReward import BlockReward


class FixedReward(BlockReward):

    def computeBlockReward(self, height, timeTocreate):
        return 1

    def reset(self): pass
