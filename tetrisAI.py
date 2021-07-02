from tetris import *
import random
import copy

class boardEval:
    
    COMPLETELINEWEIGHT = 10
    SPIKINESSWEIGHT = -0.2
    HOLEWEIGHT = -1
    
    def getColumnHeight(self, board, x):
        highestBlock = 0
        for y in range(len(board[x])):
            if board[x][y] == '.':
                highestBlock = y-1
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
    
    # Returns the highest evaluated future state
    def returnBestState(self, piece, board):
        evaluations = {}
        bestState = None
        for r in range(len(PIECES[piece['shape']])): 
            piece['rotation'] = r
            for x in range(-2, BOARDWIDTH + 2):
                newBoard = copy.deepcopy(board)
                piece['y'] = -2
                piece['x'] = x
                if not isValidPosition(board, piece):
                    continue
                for i in range(1, BOARDHEIGHT):
                    if not isValidPosition(board, piece, adjY=i):
                        break
                piece['y'] += i - 1

                addToBoard(newBoard, piece)
                evaluations[(x, r)] = self.evalBoardState(newBoard)

                if bestState == None:
                    bestState = (x, r)
                else:
                    if evaluations[(x, r)] > evaluations[bestState]:
                        bestState = (x, r)
                    
        return bestState

class gameHandler:

    be = boardEval()
    
    def __init__(self, piece, board):
        self.desiredX = random.randint(-1, BOARDWIDTH-1)
        self.desiredRot = random.randint(0, 4) % len(piece['shape'])+1
        self.piece = piece
        self.board = board

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
        self.desiredX = gameHandler.be.returnBestState(self.piece, self.board)[0]
    def setDesiredRot(self):
        self.desiredRot = gameHandler.be.returnBestState(self.piece, self.board)[1]
    def newPiece(self, newPiece, board):
        self.piece = newPiece
        self.board = board
        #self.setDesiredX()
        #self.setDesiredRot()
        self.desiredX, self.desiredRot = gameHandler.be.returnBestState(self.piece, self.board)
        


        

        





