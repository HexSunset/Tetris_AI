from game import *
from gameLogic import initPygame
from random import uniform # Get random float

class Agent():
    def __init__(self, brain, numGames = 10):
        initPygame()
        self.brain = brain # Default brain
        self.game = Game()
        self.fitness = self.returnAverageFitness(numGames)
        print(self.brain)
        print(self.fitness)

    def returnAverageFitness(self, numGames):
        totalFitness = 0.0
        for i in range(numGames):
            data = self.game.runGame(self.brain, False)
            if data[1] == 0:
                continue
            else:
                totalFitness += data[0]/data[1] # fitness is calculated by score/lines cleared
        return totalFitness / numGames

if __name__ == "__main__":
    agent = Agent()
    print(agent.returnAverageFitness(5))