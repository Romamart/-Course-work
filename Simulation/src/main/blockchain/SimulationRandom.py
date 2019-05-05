from random import Random
import math


class SimulationRandom(Random):

    # def __init__(self):
    #     super(SimulationRandom, self).__init__()

    def __init__(self, seed=None):
        super(SimulationRandom, self).__init__(seed)

    def sampleNormal(self, mu, sigma):
        return super(SimulationRandom, self).gauss(0, 1) * sigma + mu

    def sampleLogNormal(self, mu, sigma):
        return math.exp(mu + self.gauss_next * sigma)

    def sampleExponential(self, lambda1):
        return math.log(1 - super(SimulationRandom, self).triangular()) / -lambda1

    def sampleExponentialRandom(self, lambda1):
        return math.log(1 - Random.triangular(self)) / -lambda1
