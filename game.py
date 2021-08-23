# Tetromino (a Tetris clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import random, time, pygame, sys
from pygame.locals import *
from tetrisAI import *
from gameLogic import *

class Game():
    def runGame(self, brain, manual):
        # setup variables for the start of the game
        self.board = getBlankBoard()
        self.lastMoveDownTime = time.time()
        self.lastMoveSidewaysTime = time.time()
        self.lastFallTime = time.time()
        self.movingDown = False # note: there is no movingUp variable
        self.movingLeft = False
        self.movingRight = False
        self.score = 0
        self.lines = 0
        self.level, self.fallFreq = calculateLevelAndFallFreq(self.score)

        self.fallingPiece = getNewPiece()
        self.nextPiece = getNewPiece()

        self.gh = gameHandler(self.fallingPiece, self.board, brain)
        


        while True: # game loop
            if self.fallingPiece == None:
                # No falling piece in play, so start a new piece at the top
                self.fallingPiece = self.nextPiece
                self.nextPiece = getNewPiece()
                # et kaks sama juppi jarjest ei tuleks
                while self.nextPiece == self.fallingPiece:
                    self.nextPiece = getNewPiece()
                self.lastFallTime = time.time() # reset lastFallTime

                if not isValidPosition(self.board, self.fallingPiece):
                    return self.score # can't fit a new piece on the board, so game over
                self.gh.newPiece(self.fallingPiece, self.board)

            checkForQuit()
            if manual == False:
                if self.gh.rotatePiece(self.fallingPiece['rotation'], self.fallingPiece) != 0:
                    self.fallingPiece['rotation'] += self.gh.rotatePiece(self.fallingPiece['rotation'], self.fallingPiece)
                    if not isValidPosition(self.board, self.fallingPiece): # kui jupp pöörab end mängulaualt välja
                        if self.fallingPiece['x'] < BOARDWIDTH/2: # kui on vasakul pool mängulauda
                            while not isValidPosition(self.board, self.fallingPiece):
                                self.fallingPiece['x'] += 1
                        else: # jupp on paremal pool mängulauda
                            while not isValidPosition(self.board, self.fallingPiece):
                                self.fallingPiece['x'] -= 1
                elif self.gh.movePieceToPosition(self.fallingPiece['x']) == -1:
                    self.movingLeft = True
                elif self.gh.movePieceToPosition(self.fallingPiece['x']) == 1:
                    self.movingRight = True
                else: # jupp on oiges kohas ja voib alla kukutada
                        self.movingLeft = False
                        self.movingRight = False
                        for i in range(1, BOARDHEIGHT):
                            if not isValidPosition(self.board, self.fallingPiece, adjY=i):
                                break
                        self.fallingPiece['y'] += i - 1
                        if isValidPosition(self.board, self.fallingPiece, adjY=1):
                            self.fallingPiece['y'] += 1
                        addToBoard(self.board, self.fallingPiece)
                        self.scoreChange, self.linesChange = updateScore(self.board, self.level)
                        self.score += self.scoreChange
                        self.lines += self.linesChange
                        self.level, self.fallFreq = calculateLevelAndFallFreq(self.lines)
                        self.fallingPiece = None
                
                if self.movingRight:
                    if isValidPosition(self.board, self.fallingPiece, adjX=1):
                        self.fallingPiece['x'] += 1
                    if isValidPosition(self.board, self.fallingPiece, adjY=1):
                        self.fallingPiece['y'] += 1
                    else:
                        # falling piece has landed, set it on the board
                        addToBoard(self.board, self.fallingPiece)
                        self.score += removeCompleteLines(self.board)
                        self.level, self.fallFreq = calculateLevelAndFallFreq(self.score)
                        self.fallingPiece = None
                if self.movingLeft:
                    if isValidPosition(self.board, self.fallingPiece, adjX=-1):
                        self.fallingPiece['x'] -= 1
                    if isValidPosition(self.board, self.fallingPiece, adjY=1):
                        self.fallingPiece['y'] += 1
                    else:
                        # falling piece has landed, set it on the board
                        addToBoard(self.board, self.fallingPiece)
                        self.score += removeCompleteLines(self.board)
                        self.level, self.fallFreq = calculateLevelAndFallFreq(self.score)
                        self.fallingPiece = None
                    
            # Manual controls mode
            else:
                for event in pygame.event.get(): # event handling loop
                    if event.type == KEYUP:
                        if (event.key == K_p):
                            # Pausing the game
                            DISPLAYSURF.fill(BGCOLOR)
                            pygame.mixer.music.stop()
                            showTextScreen('Paused') # pause until a key press
                            pygame.mixer.music.play(-1, 0.0)
                            self.lastFallTime = time.time()
                            self.lastMoveDownTime = time.time()
                            self.lastMoveSidewaysTime = time.time()
                        elif (event.key == K_LEFT or event.key == K_a):
                            self.movingLeft = False
                        elif (event.key == K_RIGHT or event.key == K_d):
                            self.movingRight = False
                        elif (event.key == K_DOWN or event.key == K_s):
                            self.movingDown = False

                    elif event.type == KEYDOWN:
                        # moving the piece sideways
                        if (event.key == K_LEFT or event.key == K_a) and isValidPosition(self.board, self.fallingPiece, adjX=-1):
                            self.fallingPiece['x'] -= 1
                            self.movingLeft = True
                            self.movingRight = False
                            self.lastMoveSidewaysTime = time.time()

                        elif (event.key == K_RIGHT or event.key == K_d) and isValidPosition(self.board, self.fallingPiece, adjX=1):
                            self.fallingPiece['x'] += 1
                            self.movingRight = True
                            self.movingLeft = False
                            self.lastMoveSidewaysTime = time.time()

                        # rotating the piece (if there is room to rotate)
                        elif (event.key == K_UP or event.key == K_w):
                            self.fallingPiece['rotation'] = (self.fallingPiece['rotation'] + 1) % len(PIECES[self.fallingPiece['shape']])
                            if not isValidPosition(self.board, self.fallingPiece):
                                self.fallingPiece['rotation'] = (self.fallingPiece['rotation'] - 1) % len(PIECES[self.fallingPiece['shape']])
                        elif (event.key == K_q): # rotate the other direction
                            self.fallingPiece['rotation'] = (self.fallingPiece['rotation'] - 1) % len(PIECES[self.fallingPiece['shape']])
                            if not isValidPosition(self.board, self.fallingPiece):
                                self.fallingPiece['rotation'] = (self.fallingPiece['rotation'] + 1) % len(PIECES[self.fallingPiece['shape']])

                        # making the piece fall faster with the down key
                        elif (event.key == K_DOWN or event.key == K_s):
                            self.movingDown = True
                            if isValidPosition(self.board, self.fallingPiece, adjY=1):
                                self.fallingPiece['y'] += 1
                            self.lastMoveDownTime = time.time()

                        # move the current piece all the way down
                        elif event.key == K_SPACE:
                            self.movingDown = False
                            self.movingLeft = False
                            self.movingRight = False
                            for i in range(1, BOARDHEIGHT):
                                if not isValidPosition(self.board, self.fallingPiece, adjY=i):
                                    break
                            self.fallingPiece['y'] += i - 1

                # handle moving the piece because of user input
                if (self.movingLeft or self.movingRight) and time.time() - self.lastMoveSidewaysTime > MOVESIDEWAYSFREQ:
                    if self.movingLeft and isValidPosition(self.board, self.fallingPiece, adjX=-1):
                        self.fallingPiece['x'] -= 1
                    elif self.movingRight and isValidPosition(self.board, self.fallingPiece, adjX=1):
                        self.fallingPiece['x'] += 1
                    self.lastMoveSidewaysTime = time.time()

                if self.movingDown and time.time() - self.lastMoveDownTime > MOVEDOWNFREQ and isValidPosition(self.board, self.fallingPiece, adjY=1):
                    self.fallingPiece['y'] += 1
                    self.lastMoveDownTime = time.time()

                # let the piece fall if it is time to fall
                if time.time() - self.lastFallTime > self.fallFreq:
                    # see if the piece has landed
                    if not isValidPosition(self.board, self.fallingPiece, adjY=1):
                        # falling piece has landed, set it on the board
                        addToBoard(self.board, self.fallingPiece)
                        self.score += removeCompleteLines(self.board)
                        self.level, self.fallFreq = calculateLevelAndFallFreq(self.score)
                        self.fallingPiece = None
                    else:
                        # piece did not land, just move the piece down
                        self.fallingPiece['y'] += 1
                        self.lastFallTime = time.time()
            self.movingDown = False
            self.movingLeft = False
            self.movingRight = False

            # drawing everything on the screen
            fillBG()
            drawBoard(self.board)
            drawStatus(self.score, self.lines, self.level)
            drawNextPiece(self.nextPiece)
            if self.fallingPiece != None:
                drawPiece(self.fallingPiece)
            updateDisplay()


def main():
    initPygame()
    game = Game()
    # Check for the noai launch option, disable ai
    global manual_mode
    if len(sys.argv) > 1: 
        if sys.argv[1] == "-noai":
            manual_mode = True
    else:
        manual_mode = False

    showTextScreen('Tetromino')
    while True: # game loop
#        if random.randint(0, 1) == 0:
#            pygame.mixer.music.load('tetrisb.mid')
#        else:
#            pygame.mixer.music.load('tetrisc.mid')
#        pygame.mixer.music.play(-1, 0.0)
#        pygame.mixer.music.stop()
        score = game.runGame([1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0 ], manual_mode)
        print("Score:",score)
        showTextScreen('Game Over')

if __name__ == '__main__':
    main()
