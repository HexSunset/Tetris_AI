from game import *
from gameLogic import initPygame
from random import uniform # Get random float

class Agent():
    def __init__(self, brain, numGames = 2):
        initPygame()
        self.brain = brain # Default brain
        self.game = Game()
        self.fitness = self.returnAverageScore(numGames)
        print(self.brain)
        print(self.fitness)

    def returnAverageScore(self, numGames):
        totalScore = 0.0
        for i in range(numGames):
            totalScore += self.game.runGame(self.brain, False)
        return totalScore / numGames

if __name__ == "__main__":
    agent = Agent()
    print(agent.returnAverageScore(5))