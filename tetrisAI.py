from gameLogic import *
import random
import copy

class boardEval:
    
    COMPLETELINEWEIGHT = 10
    SPIKINESSWEIGHT = -0.1
    HOLEWEIGHT = -0.2
    HEIGHTWEIGHT = -100

    def __init__(self, brain):
        self.brain = brain

    def getColumnHeight(self, board, x):
        for y in range(len(board[x])):
            if board[x][y] != BLANK:
                return BOARDHEIGHT - y
        return 0
        
    
    def getNumberOfHoles(self, board, x):
        columnHeight = self.getColumnHeight(board, x)
        numberOfHoles = 0
        for y in range(columnHeight):
            if board[x][y] == BLANK:
                numberOfHoles += 1
        return numberOfHoles

    def getBoardState(self, board):
        numLinesCleared = 0
        for y in range(BOARDHEIGHT):
            if isCompleteLine(board, y):
                numLinesCleared += boardEval.COMPLETELINEWEIGHT #calculate number of completed lines

        totalColHeight = 0
        numPits = 0
        for x in range(BOARDWIDTH):
            totalColHeight += self.getColumnHeight(board, x) #calculate aggregate column height
            if self.getColumnHeight(board, x) == 0:
                numPits += 1
        averageColHeight = totalColHeight/BOARDWIDTH

        bumpiness = 0
        for x in range(BOARDWIDTH):
            bumpiness += abs(self.getColumnHeight(board, x) - averageColHeight) #calculate bumpiness of the board
        
        numberOfHoles = 0
        numColsWithAtLeastOneHole = 0
        for x in range(BOARDWIDTH):
            numberOfHoles += self.getNumberOfHoles(board, x) #calculate number of holes
            if self.getNumberOfHoles(board, x) != 0:
                numColsWithAtLeastOneHole += 1

        rowTransitions = 0
        for y in range(BOARDHEIGHT):
            for x in range(BOARDWIDTH-1):
                if (board[x][y] == BLANK) != (board[x+1][y] == BLANK): #if this tile has a block and the next tile doesn't have a block or od this tile doesn't have a block and the next tile does
                    rowTransitions += 1

        colTransitions = 0
        for y in range(BOARDHEIGHT-1):
            for x in range(BOARDWIDTH):
                if (board[x][y] == BLANK) != (board[x][y+1] == BLANK): #if this tile has a block and the next tile doesn't have a block or od this tile doesn't have a block and the next tile does
                    colTransitions += 1
        
        deepestWell = 0
        for x in range(BOARDWIDTH):
            currentHeight = self.getColumnHeight(board, x)
            if x == 0:
                currentWell = self.getColumnHeight(board, x+1)-currentHeight
            elif x == BOARDWIDTH-1:
                currentWell = self.getColumnHeight(board, x-1)-currentHeight
            else:
                currentWell = max([self.getColumnHeight(board, x+1), self.getColumnHeight(board, x-1)])-currentHeight
            if currentWell > deepestWell:
                deepestWell = currentWell


        
        return [numLinesCleared, totalColHeight, numPits, bumpiness, numberOfHoles, numColsWithAtLeastOneHole, rowTransitions, colTransitions, deepestWell]
    
    def evalState(self, board, brain):
        stateVariables = self.getBoardState(board)
        score = 0
        for i in range(len(stateVariables)):
            score += stateVariables[i] * brain[i]
        
        return score

    # Returns the highest evaluated future state
    def returnBestState(self, piece, board):
        evaluations = {}
        bestState = None
        start_x = piece['x']
        old_y = piece['y']
        for r in range(len(PIECES[piece['shape']])): 
            piece['rotation'] = r
            for target_x in range(-2, BOARDWIDTH + 2):
                newBoard = copy.deepcopy(board)
                piece['y'] = 0
                piece['x'] = start_x
                if not isValidPosition(board, piece):
                    continue
                curr_x = start_x
                i = 0
                while curr_x != target_x:
                    i += 1
                    if target_x > curr_x:
                        curr_x += 1
                    else:
                        curr_x -= 1
                    if not isValidPosition(board, piece, adjY=i, adjX=(curr_x - start_x)):
                        curr_x = target_x + 1 # Make sure they don't match
                        break
                if curr_x != target_x:
                    continue
                piece['x'] = target_x
                for i in range(1, BOARDHEIGHT):
                    if not isValidPosition(board, piece, adjY=i):
                        break
                piece['y'] += i - 1

                addToBoard(newBoard, piece)
                evaluations[(target_x, r)] = self.evalState(newBoard, self.brain)

                if bestState == None:
                    bestState = (target_x, r)
                else:
                    if evaluations[(target_x, r)] > evaluations[bestState]:
                        bestState = (target_x, r)
        piece['x'] = start_x
        piece['y'] = old_y
        print(PIECES[piece['shape']][piece['rotation']])
        print(board)

        print(evaluations)
        return bestState

class gameHandler:
    
    def __init__(self, piece, board, brain):
        self.be = boardEval(brain)
        self.piece = piece
        self.board = board

        self.desiredX, self.desiredRot = self.be.returnBestState(piece, board)

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
        self.desiredX = self.be.returnBestState(self.piece, self.board)[0]
    def setDesiredRot(self):
        self.desiredRot = self.be.returnBestState(self.piece, self.board)[1]
    def newPiece(self, newPiece, board):
        self.piece = newPiece
        self.board = board
        #self.setDesiredX()
        #self.setDesiredRot()
        self.bestState = self.be.returnBestState(self.piece, self.board)
        if self.bestState == None: #No valid moves
            self.bestState = (self.piece['x'], self.piece['rotation'])
        self.desiredX, self.desiredRot = self.bestState
        


        

        





