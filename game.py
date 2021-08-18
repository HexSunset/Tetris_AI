# Tetromino (a Tetris clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import random, time, pygame, sys
from pygame.locals import *
from tetrisAI import *
from gameLogic import *

class Game():
    def runGame(this):
        # setup variables for the start of the game
        this.board = getBlankBoard()
        this.lastMoveDownTime = time.time()
        this.lastMoveSidewaysTime = time.time()
        this.lastFallTime = time.time()
        this.movingDown = False # note: there is no movingUp variable
        this.movingLeft = False
        this.movingRight = False
        this.score = 0
        this.level, this.fallFreq = calculateLevelAndFallFreq(this.score)

        this.fallingPiece = getNewPiece()
        this.nextPiece = getNewPiece()

        this.gh = gameHandler(this.fallingPiece, this.board)
        


        while True: # game loop
            if this.fallingPiece == None:
                # No falling piece in play, so start a new piece at the top
                this.fallingPiece = this.nextPiece
                this.nextPiece = getNewPiece()
                # et kaks sama juppi jarjest ei tuleks
                while this.nextPiece == this.fallingPiece:
                    this.nextPiece = getNewPiece()
                this.lastFallTime = time.time() # reset lastFallTime

                if not isValidPosition(this.board, this.fallingPiece):
                    return # can't fit a new piece on the board, so game over
                this.gh.newPiece(this.fallingPiece, this.board)

            checkForQuit()
            if manual_mode == False:
                if this.gh.rotatePiece(this.fallingPiece['rotation'], this.fallingPiece) != 0:
                    this.fallingPiece['rotation'] += this.gh.rotatePiece(this.fallingPiece['rotation'], this.fallingPiece)
                    if not isValidPosition(this.board, this.fallingPiece): # kui jupp pöörab end mängulaualt välja
                        if this.fallingPiece['x'] < BOARDWIDTH/2: # kui on vasakul pool mängulauda
                            while not isValidPosition(this.board, this.fallingPiece):
                                this.fallingPiece['x'] += 1
                        else: # jupp on paremal pool mängulauda
                            while not isValidPosition(this.board, this.fallingPiece):
                                this.fallingPiece['x'] -= 1
                elif this.gh.movePieceToPosition(this.fallingPiece['x']) == -1:
                    this.movingLeft = True
                elif this.gh.movePieceToPosition(this.fallingPiece['x']) == 1:
                    this.movingRight = True
                else: # jupp on oiges kohas ja voib alla kukutada
                        this.movingLeft = False
                        this.movingRight = False
                        for i in range(1, BOARDHEIGHT):
                            if not isValidPosition(this.board, this.fallingPiece, adjY=i):
                                break
                        this.fallingPiece['y'] += i - 1
                        if isValidPosition(this.board, this.fallingPiece, adjY=1):
                            this.fallingPiece['y'] += 1
                        addToBoard(this.board, this.fallingPiece)
                        this.score += removeCompleteLines(this.board)
                        this.level, this.fallFreq = calculateLevelAndFallFreq(this.score)
                        this.fallingPiece = None
                
                if this.movingRight:
                    if isValidPosition(this.board, this.fallingPiece, adjX=1):
                        this.fallingPiece['x'] += 1
                    if isValidPosition(this.board, this.fallingPiece, adjY=1):
                        this.fallingPiece['y'] += 1
                    else:
                        # falling piece has landed, set it on the board
                        addToBoard(this.board, this.fallingPiece)
                        this.score += removeCompleteLines(this.board)
                        this.level, this.fallFreq = calculateLevelAndFallFreq(this.score)
                        this.fallingPiece = None
                if this.movingLeft:
                    if isValidPosition(this.board, this.fallingPiece, adjX=-1):
                        this.fallingPiece['x'] -= 1
                    if isValidPosition(this.board, this.fallingPiece, adjY=1):
                        this.fallingPiece['y'] += 1
                    else:
                        # falling piece has landed, set it on the board
                        addToBoard(this.board, this.fallingPiece)
                        this.score += removeCompleteLines(this.board)
                        this.level, this.fallFreq = calculateLevelAndFallFreq(this.score)
                        this.fallingPiece = None
                    
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
                            this.lastFallTime = time.time()
                            this.lastMoveDownTime = time.time()
                            this.lastMoveSidewaysTime = time.time()
                        elif (event.key == K_LEFT or event.key == K_a):
                            this.movingLeft = False
                        elif (event.key == K_RIGHT or event.key == K_d):
                            this.movingRight = False
                        elif (event.key == K_DOWN or event.key == K_s):
                            this.movingDown = False

                    elif event.type == KEYDOWN:
                        # moving the piece sideways
                        if (event.key == K_LEFT or event.key == K_a) and isValidPosition(this.board, this.fallingPiece, adjX=-1):
                            this.fallingPiece['x'] -= 1
                            this.movingLeft = True
                            this.movingRight = False
                            this.lastMoveSidewaysTime = time.time()

                        elif (event.key == K_RIGHT or event.key == K_d) and isValidPosition(this.board, this.fallingPiece, adjX=1):
                            this.fallingPiece['x'] += 1
                            this.movingRight = True
                            this.movingLeft = False
                            this.lastMoveSidewaysTime = time.time()

                        # rotating the piece (if there is room to rotate)
                        elif (event.key == K_UP or event.key == K_w):
                            this.fallingPiece['rotation'] = (this.fallingPiece['rotation'] + 1) % len(PIECES[this.fallingPiece['shape']])
                            if not isValidPosition(this.board, this.fallingPiece):
                                this.fallingPiece['rotation'] = (this.fallingPiece['rotation'] - 1) % len(PIECES[this.fallingPiece['shape']])
                        elif (event.key == K_q): # rotate the other direction
                            this.fallingPiece['rotation'] = (this.fallingPiece['rotation'] - 1) % len(PIECES[this.fallingPiece['shape']])
                            if not isValidPosition(this.board, this.fallingPiece):
                                this.fallingPiece['rotation'] = (this.fallingPiece['rotation'] + 1) % len(PIECES[this.fallingPiece['shape']])

                        # making the piece fall faster with the down key
                        elif (event.key == K_DOWN or event.key == K_s):
                            this.movingDown = True
                            if isValidPosition(this.board, this.fallingPiece, adjY=1):
                                this.fallingPiece['y'] += 1
                            this.lastMoveDownTime = time.time()

                        # move the current piece all the way down
                        elif event.key == K_SPACE:
                            this.movingDown = False
                            this.movingLeft = False
                            this.movingRight = False
                            for i in range(1, BOARDHEIGHT):
                                if not isValidPosition(this.board, this.fallingPiece, adjY=i):
                                    break
                            this.fallingPiece['y'] += i - 1

                # handle moving the piece because of user input
                if (this.movingLeft or this.movingRight) and time.time() - this.lastMoveSidewaysTime > MOVESIDEWAYSFREQ:
                    if this.movingLeft and isValidPosition(this.board, this.fallingPiece, adjX=-1):
                        this.fallingPiece['x'] -= 1
                    elif this.movingRight and isValidPosition(this.board, this.fallingPiece, adjX=1):
                        this.fallingPiece['x'] += 1
                    this.lastMoveSidewaysTime = time.time()

                if this.movingDown and time.time() - this.lastMoveDownTime > MOVEDOWNFREQ and isValidPosition(this.board, this.fallingPiece, adjY=1):
                    this.fallingPiece['y'] += 1
                    this.lastMoveDownTime = time.time()

                # let the piece fall if it is time to fall
                if time.time() - this.lastFallTime > this.fallFreq:
                    # see if the piece has landed
                    if not isValidPosition(this.board, this.fallingPiece, adjY=1):
                        # falling piece has landed, set it on the board
                        addToBoard(this.board, this.fallingPiece)
                        this.score += removeCompleteLines(this.board)
                        this.level, this.fallFreq = calculateLevelAndFallFreq(this.score)
                        this.fallingPiece = None
                    else:
                        # piece did not land, just move the piece down
                        this.fallingPiece['y'] += 1
                        this.lastFallTime = time.time()
            this.movingDown = False
            this.movingLeft = False
            this.movingRight = False

            # drawing everything on the screen
            fillBG()
            drawBoard(this.board)
            drawStatus(this.score, this.level)
            drawNextPiece(this.nextPiece)
            if this.fallingPiece != None:
                drawPiece(this.fallingPiece)
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
        game.runGame()
        showTextScreen('Game Over')

if __name__ == '__main__':
    main()
