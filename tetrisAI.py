from tetris import *
import random

class gameHandler:
        
    def __init__(self, piece):
        self.desiredX = random.randint(-1, BOARDWIDTH-1)
        self.desiredRot = random.randint(0, 4) % len(piece['shape'])+1
        self.piece = piece

    def movePieceToPosition(self, pieceX): #returns -1 if moving left, 1 if moving right, and 0 if the x coordinate is correct
        if pieceX > self.desiredX:
            return -1
        elif pieceX < self.desiredX:
            return 1
        else:
            return 0
    def rotatePiece(self, pieceRotation, piece): #returns -1 if rotating left, 1 if rotating right, and 0 if its correctly rotated
        if piece['shape'] == 'O':
            return 0
        if self.desiredRot == pieceRotation:
            return 0
        elif self.desiredRot - pieceRotation < 3:
            return int(abs(self.desiredRot - pieceRotation) / (self.desiredRot - pieceRotation))
        else:
            return int(abs(self.desiredRot - pieceRotation) / -(self.desiredRot - pieceRotation))
    def setDesiredX(self):
        self.desiredX = random.randint(-1, BOARDWIDTH-1)
    def setDesiredRot(self):
        self.desiredRot = random.randint(0, 4) % len(self.piece['shape'])
    def newPiece(self, newPiece):
        self.setDesiredX()
        self.setDesiredRot()
        self.piece = newPiece

class boardEval:
    
    COMPLETELINEWEIGHT = 10
    SPIKINESSWEIGHT = -0.2
    HOLEWEIGHT = -1
    
    def getColumnHeight(board, x):
        highestBlock = 0
        for y in range(len(board[x])):
            if board[x][y] == 'O':
                highestBlock = y
        return highestBlock
    
    def getNumberOfHoles(self, board, x):
        columnHeight = self.getColumnHeight(board, x)
        numberOfHoles = 0
        for y in range(columnHeight):
            if board[x][y] == BLANK:
                numberOfHoles += 1
        return numberOfHoles

    def evalBoardState(self, board):
        currentEval = 0
        for y in range(BOARDHEIGHT):
            if isCompleteLine(board, y):
                currentEval += boardEval.COMPLETELINEWEIGHT #add to currentEval if there are completed lines

        averageColWidth = 0
        for x in range(BOARDWIDTH):
            averageColWidth += self.getColumnHeight(board, x)
        averageColWidth /= BOARDWIDTH

        for x in range(BOARDWIDTH):
            currentEval += abs(self.getColumnHeight(board, x) - averageColWidth) * boardEval.SPIKINESSWEIGHT #subtract from currentEval based on the "spikiness" of the board
        
        numberOfHoles = 0
        for x in range(BOARDWIDTH):
            numberOfHoles += self.getNumberOfHoles(board, x)
        currentEval += numberOfHoles * boardEval.HOLEWEIGHT
        
        return currentEval

        

        





