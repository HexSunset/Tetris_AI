from tetris import *
import random

class gameHandler:
        
    def __init__(self, piece):
        self.desiredX = random.randint(BOARDWIDTH)
        self.desiredRot = random.randint(4) % len(piece['shape'])
        self.piece = piece

    def movePieceToPosition(self, pieceX): # tagastab -1 kui on vaja liikuda vasakule, 1 kui on liikuda paremale ja 0 kui on jupp õiges kohas.
        if pieceX > self.desiredX:
            return -1
        elif pieceX < self.desiredX:
            return 1
        else:
            return 0
    def rotatePiece(self, pieceRotation, piece): # tagastab -1 kui on vaja pöörata ühele poole, 1 kui on vaja pöörata teisele poole
        if self.desiredRot == pieceRotation:
            return 0
        # nelja võimaliku rotatsiooni puhul on võimalik alati tahetud rotatsioonini kahe pöördega saada
        # kolme ja vähema puhul kulub selleks ainult üks
        elif self.desiredRot - pieceRotation < 3:
            return abs(self.desiredRot - pieceRotation) / (self.desiredRot - pieceRotation)
        else:
            return abs(self.desiredRot - pieceRotation) / -(self.desiredRot - pieceRotation)
    def setDesiredX(self):
        self.desiredX = random.randint(BOARDWIDTH) #selle leiab hiljem AIga
        #               ^ (todo) siit tuleb lahutada jupi laius muidu võib jupp mängualalt välja minna
    def setDesiredRot(self):
        self.desiredRot = random.randint(4) % len(self.piece['shape']) # leitud on jääk, juhul kui jupil on vähem kui 4 võimalikku rotatsiooni
    def newPiece(self, newPiece):
        self.setDesiredX()
        self.setDesiredRot()
        self.piece = newPiece

