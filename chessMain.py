#it is use to show the current game state by using pygame
import colorsys
import pygame as p
import chessEngine
import smartmovefinder
W=400
H=400
D=8 # 8x8 board
SQ_SIZE=W//D# each square size
MAX_FPS=15#used for animation
IMAGES={} # TO STORE THE LOADED IMAGES 
def load_images():
    pieces=["wR","wN","wB","wQ","wK","wP","bP","bK","bQ","bB","bN","bR"]
    for i in pieces:
        IMAGES[i]=p.transform.scale(p.image.load("images/"+i+".png"),(SQ_SIZE,SQ_SIZE))
    
def main():
    p.init()
    screen=p.display.set_mode((W,H))
    p.display.set_caption("chess")
    img=p.image.load("images/chess.png")
    p.display.set_icon(img)
    clock=p.time.Clock()
    screen.fill(p.Color("white"))
    load_images()
    gs=chessEngine.GameState()
    validMoves=gs.getValidMoves()
    movemade=False#tosee whther a move is made or not
    animate=False
    running=True
    sqSelected=()#to store mouse co-ordinates as (x,y)
    PlayerClicks=[]#stores tuples of (x,y)
    gameover=False
    playerOne=True
    playerTwo=False
    while running:
        humanTurn=(gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        for i in p.event.get():
            if(i.type==p.QUIT):
                running=False  
            elif(i.type==p.MOUSEBUTTONDOWN):
                if not gameover and humanTurn:
                    location=p.mouse.get_pos()
                    col=location[0]//SQ_SIZE
                    row=location[1]//SQ_SIZE
                    if(sqSelected==(row,col)):
                        sqSelected=()
                        PlayerClicks=[]
                    else:
                        sqSelected=(row,col)
                        PlayerClicks.append(sqSelected)
                    if(len(PlayerClicks)==2):
                        move=chessEngine.Move(PlayerClicks[0],PlayerClicks[1],gs.board)
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                movemade=True
                                animate=True
                                print(move.getChessnotation())
                                sqSelected=()
                                PlayerClicks=[]
                        if not movemade:
                            PlayerClicks=[sqSelected]
            elif (i.type==p.KEYDOWN):
                if (i.key==p.K_u):#press u to undo the move
                    gs.undo()
                    movemade=True
                    animate=False
                if i.key==p.K_r:
                    gs=chessEngine.GameState()
                    validMoves=gs.getValidMoves()
                    sqSelected=()
                    PlayerClicks=[]
                    movemade=False
                    animate=False
            #AI MOVE FINDER
            if not gameover and not humanTurn:
                AIMove=smartmovefinder.findBestMove(gs,validMoves)
                if(AIMove is None):
                    AIMove=smartmovefinder.findrandommove(validMoves)
                gs.makeMove(AIMove)
                movemade=True
                animate=True
            if movemade:
                if(animate):
                    animateMove(gs.movelog[-1],screen,gs.board,clock)
                validMoves=gs.getValidMoves()
                movemade=False
                animate=False
                
        drawGameState(screen,gs,validMoves,sqSelected)
        if gs.checkMate:
            gameover=True
            if gs.whiteToMove:
                drawText(screen,"blacks win by checkmate")
            else:
                drawText(screen,"whites wins by checkmate")
        if(gs.staleMate):
            gameover=True
            drawText(screen,"draw")
        clock.tick(MAX_FPS)
        p.display.flip()
def higlightSquares(screen,gs,validMoves,sqselected):
    if(sqselected!=()):
        r,c=sqselected
        if gs.board[r][c][0]==("w"if gs.whiteToMove else "b"):
            s=p.Surface((SQ_SIZE,SQ_SIZE))
            s.set_alpha(150)#0->transparency 255->opaque
            s.fill(p.Color("blue"))
            screen.blit(s,(c*SQ_SIZE,r*SQ_SIZE))
            s.fill(p.Color("orange"))
            for move in validMoves:
                if(move.startRow==r and move.startCol==c):
                    screen.blit(s,(move.endCol*SQ_SIZE,move.endRow*SQ_SIZE))
                
                    
def drawGameState(screen,gs,validMoves,sqselected):
    drawBoard(screen)
    higlightSquares(screen,gs,validMoves,sqselected)
    drawPieces(screen,gs.board)
def drawBoard(screen):
    global colours
    colours=[p.Color("gray"),p.Color("white")]
    for r in range(D):
        for c in range(D):
            colour=colours[(r+c)%2]
            p.draw.rect(screen,colour,p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))
def drawPieces(screen,board):
    for r in range(D):
        for c in range(D):
            piece=board[r][c]
            if(piece!="--"):
                screen.blit(IMAGES[piece],p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))
def animateMove(move,screen,board,clock):
    global colours
    dr=move.endRow - move.startRow
    dc=move.endCol-move.startCol
    framePerSquare=10 #frames tro move one square
    frameCount=(abs(dr)+abs(dc))*framePerSquare
    for frame in range(frameCount+1):
        r,c=(move.startRow+dr*(frame/frameCount),move.startCol+dc*(frame/frameCount))
        drawBoard(screen)
        drawPieces(screen,board)
        color=colours[(move.endRow + move.endCol)%2]
        endSquare=p.Rect(move.endCol*SQ_SIZE,move.endCol*SQ_SIZE,SQ_SIZE,SQ_SIZE)
        p.draw.rect(screen,color,endSquare)
        if move.capturedpiece!="--":
            screen.blit(IMAGES[move.capturedpiece],endSquare)
        #draw moving pieces
        screen.blit(IMAGES[move.movedpiece],p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))
        #p.display.flip()
        #clock.tick(60)
def drawText(screen,text):
    font=p.font.SysFont("Molvitca",32,True,False)
    textObject=font.render(text,0,p.Color("red"))
    textLocation=p.Rect(0,0,W,H).move(W/2-textObject.get_width()/2,H/2-textObject.get_height()/2)
    screen.blit(textObject,textLocation)
    textObject=font.render(text,0,p.Color("yellow"))
    screen.blit(textObject,textLocation.move(2,2))

if __name__=="__main__":
    main()
        
            
        
    

        
    