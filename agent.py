from game import *
from gameLogic import initPygame

class Agent():
    def __init__(self, brain):
        initPygame()
        self.brain = brain
        self.game = Game()

    def returnAverageScore(self, numGames):
        totalScore = 0.0
        for i in range(numGames):
            totalScore += self.game.runGame(self.brain, False)
        return totalScore / numGames


if __name__ == "__main__":
    agent = Agent([1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0 ])
    print(agent.returnAverageScore(5))