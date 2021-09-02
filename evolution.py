from hashlib import new
from typing import DefaultDict
from agent import Agent
import random
import sys

class Evolution():
    def __init__(self):
        self.file = open("evolutiondata.txt", "a")
        
        # Check launch options for custom values
        if len(sys.argv) > 1:
            if '-b' in sys.argv:
                self.defaultBrain = list(map(float,sys.argv[sys.argv.index('-b') + 1].split(',')))
            else:
                self.defaultBrain = [0, 0, 0, 0, 0, 0, 0, 0, 0]
            if '-s' in sys.argv:
                self.genSize = int(sys.argv[sys.argv.index('-s') + 1])
            else:
                self.genSize = 10
            if '-c' in sys.argv:
                genCount = int(sys.argv[sys.argv.index('-c') + 1])
            else:
                genCount = 4
        else:
            self.defaultBrain = [0, 0, 0, 0, 0, 0, 0, 0, 0]
            self.genSize = 15
            genCount = 50

        print("1. generation")
        self.file.write("1. generation\n")
        self.gen = self.createFirstGen(self.genSize)

        for i in range(1, genCount):
            print(str(i + 1) + ". generation")
            self.file.write("\n" + str(i + 1) + ". generation\n")
            self.getElite()
            self.populateGeneration()
            
        self.file.close()
        return

    def createFirstGen(self, genSize):
        newGen = []
        for i in range(genSize):
            newGen.append(Agent(self.createChild(self.defaultBrain, self.defaultBrain)))
            self.file.write(str(newGen[-1].brain) + "\n")
            self.file.write(str(newGen[-1].fitness) + "\n")
            self.file.flush()
        return newGen
    
    def populateGeneration(self):
        # Show the agents that were taken over from the last generation
        for agent in self.gen:
            print(agent.brain)
            print(agent.fitness)
            self.file.write(str(agent.brain) + "\n")
            self.file.write(str(agent.fitness) + "\n")

        # Fill up the generation
        for i in range(self.genSize - len(self.gen)):

            # Probability distribution for parents
            roll = random.uniform(0,1)
            parentA = None
            parentB = None
            for i in range(len(self.gen)):
                if roll > 0.5**(i+1):
                    parentA = self.gen[i]
                    break
            if parentA == None:
                parentA = self.gen[len(self.gen)-1]

            roll = random.uniform(0,1)
            for i in range(len(self.gen)):
                if roll > 0.5**(i+1):
                    parentB = self.gen[i]
                    break
            if parentB == None:
                parentB = self.gen[len(self.gen)-1]

            self.gen.append(Agent(self.createChild(parentA.brain, parentB.brain)))
            self.file.write(str(self.gen[-1].brain) + "\n")
            self.file.write(str(self.gen[-1].fitness) + "\n")
            self.file.flush()
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
    evolver = Evolution()