from hashlib import new
from typing import DefaultDict
from agent import Agent
import random

class Evolution():
    def __init__(self, genSize, genCount = 5):
        self.defaultBrain = [1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0]
        self.genSize = genSize
        print("1. generation")
        self.gen = self.createFirstGen(genSize)
        for i in range(1, genCount):
            print(str(i + 1) + ". generation")
            self.getElite()
            self.populateGeneration()
            print("\n")
        print("-----------------------------")
        for agent in self.gen:
            print(agent.brain)
            print(agent.fitness)
        return

    def createFirstGen(self, genSize):
        newGen = []
        for i in range(genSize):
            newGen.append(Agent(self.createChild(self.defaultBrain, self.defaultBrain)))
        return newGen
    
    def populateGeneration(self):
        # Fill up the generation
        for i in range(self.genSize - len(self.gen)):
            self.gen.append(Agent(self.createChild(random.choice(self.gen).brain, random.choice(self.gen).brain)))
    
    # Take in 2 parent brains, combine them into a child, mutate child
    def createChild(self, parentA, parentB):
        childBrain = []
        for i in range(9):
            if random.randint(0,1) == 1:
                childBrain.append(parentA[i])
            else:
                childBrain.append(parentB[i])

            # 20% chance to mutate
            if random.uniform(0.0, 1.0) <= 0.2:
                childBrain[i] += round(random.uniform(-0.2, 0.2), 2)
        return childBrain

    # Remove all but the top 20% of agents
    def getElite(self, elitism = 0.2):
        # Sort generation based on fitness
        self.gen.sort(key=lambda x: x.fitness, reverse=True)
        # Remove all agents after the top 20%
        del self.gen[round(self.genSize * elitism):self.genSize]


if __name__ == "__main__":
    evolver = Evolution(10)