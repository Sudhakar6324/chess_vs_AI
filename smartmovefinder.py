from logging.config import valid_ident
import random
pieceScore={"K":0,"N":3,"Q":10,"R":5,"P":1,"B":3}
CHECKMATE=1000
STALEMATE=0
def findrandommove(validMoves):
    return validMoves[random.randint(0,len(validMoves)-1)]
def findBestMove(gs,validMoves):
    turnMultiplier=1 if gs.whiteToMove else -1
    maxscore=-CHECKMATE
    bestmove=None
    random.shuffle(validMoves)
    opponentminmaxscore=CHECKMATE
    for playermove in validMoves:
        gs.makeMove(playermove)
        opponentsMoves=gs.getValidMoves()
        opponentmaxscore= -CHECKMATE
        for opponentsmove in opponentsMoves:
            gs.makeMove(opponentsmove)
            if(gs.checkMate):
                score=-turnMultiplier*CHECKMATE
            elif(gs.staleMate):
                score=STALEMATE
            else:
                score=-turnMultiplier*scoreMaterial(gs.board)
            if(score>opponentmaxscore):
                opponentmaxscore=score
            gs.undo()
        if opponentminmaxscore>opponentmaxscore:
            opponentminmaxscore=opponentmaxscore
            bestmove=playermove
        gs.undo()
    return bestmove
        
    
def scoreMaterial(board):
    score=0
    for row in board:
        for square in row:
            if(square[0]=="w"):
                score+=pieceScore[square[1]]
            if(square[0]=="b"):
                score-=pieceScore[square[1]]
    return score
    