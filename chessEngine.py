#it stores current state of board
class GameState:
    def __init__(self):
        self.board=[
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bP","bP","bP","bP","bP","bP","bP","bP"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wP","wP","wP","wP","wP","wP","wP","wP"],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"]
        ]
        self.whiteToMove=True
        self.movelog=[]
        self.functions={"P":self.getPawnMoves,"N":self.getKnightMoves,"R":self.getRookMoves,"B":self.getBishopMoves,"Q":self.getQueenMoves,"K":self.getKingMoves}
        #to store kings location
        self.whiteKingLocation=(7,4)
        self.blackKingLocation=(0,4)
        self.checkMate=False
        self.staleMate=False
        self.empassantMove=()#for empassant move    ``````
        self.castelingRights=CastleRights(True,True,True,True)
        self.castleRightLogs=[CastleRights(self.castelingRights.wks,self.castelingRights.bks,self.castelingRights.wqs,self.castelingRights.bqs)]
    def makeMove(self,move):
        self.board[move.startRow][move.startCol]="--"
        self.board[move.endRow][move.endCol]=move.movedpiece
        self.movelog.append(move)
        self.whiteToMove = not self.whiteToMove
        #to update king location
        if(move.movedpiece=="wK"):
            self.whiteKingLocation=(move.endRow,move.endCol)
        elif(move.movedpiece=="bK"):
            self.blackKingLocation=(move.endRow,move.endCol)
        #forpawn promotion
        if(move.ispawnpromotion):
            self.board[move.endRow][move.endCol]=move.movedpiece[0]+"Q"
        # for emppasant move
        if(move.isEmpassantMove):
            self.board[move.startRow][move.endCol]="--"
        #udpate empassant move location
        if(move.movedpiece[1]=="P" and abs(move.startRow-move.endRow)==2):
            self.empassantMove=((move.startRow+move.endRow)//2,move.startCol)
        else:
            self.empassantMove=()
        if move.isCastle:
            if move.endCol-move.startCol==2:#king side castle
                self.board[move.endRow][move.endCol-1]=self.board[move.endRow][move.endCol+1]#moves the rook
                self.board[move.endRow][move.endCol+1]="--"#erase old rook
            else:
                self.board[move.endRow][move.endCol+1]=self.board[move.endRow][move.endCol-2]#moves the rook
                self.board[move.endRow][move.endCol-2]="--"#erase the rook
        self.updateCastleMove(move)
        self.castleRightLogs.append(CastleRights(self.castelingRights.wks,self.castelingRights.bks,self.castelingRights.wqs,self.castelingRights.bqs))
        
    #to update castle moves
    def updateCastleMove(self,move):
        if(move.movedpiece=="bK"):
            self.castelingRights.bks=False
            self.castelingRights.bqs=False
        elif(move.movedpiece=="wK"):
            self.castelingRights.wks=False
            self.castelingRights.wqs=False
        elif(move.movedpiece=="wR"):#white quuen side
            if(move.startRow==7):
                if(move.startCol==0):
                    self.castelingRights.wqs=False
                elif(move.startCol==7):
                    self.castelingRights.wks=False
        elif(move.movedpiece=="bR"):
            if(move.startRow==0):
                if(move.startCol==0):
                    self.castelingRights.bqs=False
                elif(move.startCol==7):
                    self.castelingRights.bks=False
                
                
            
    #undo moves
    def undo(self):
        if(len(self.movelog)!=0):
            move=self.movelog.pop()
            self.board[move.startRow][move.startCol]=move.movedpiece
            self.board[move.endRow][move.endCol]=move.capturedpiece
            self.whiteToMove=not self.whiteToMove
            if(move.movedpiece=="wK"):
                self.whiteKingLocation=(move.startRow,move.startCol)
            elif(move.movedpiece=="bK"):
                self.blackKingLocation=(move.startRow,move.startCol)
            #for empassant move
            if(move.isEmpassantMove):
                self.board[move.endRow][move.endCol]="--"
                self.board[move.startRow][move.endCol]=  move.capturedpiece
                self.empassantMove=(move.endRow,move.endCol)
            #to update empassant location
            if (move.movedpiece[1]=="P" and abs(move.startRow-move.endRow)==2):
                 self.empassantMove=()
            self.castleRightLogs.pop()
            self.castelingRights=self.castleRightLogs[-1]
            if(move.isCastle):
                if(move.endCol-move.startCol==2):#kings side
                    self.board[move.endRow][move.endCol+1]=self.board[move.endRow][move.endCol-1]
                    self.board[move.endRow][move.endCol-1]="--"
                else:#queens side
                    self.board[move.endRow][move.endCol-2]=self.board[move.endRow][move.endCol+1]
                    self.board[move.endRow][move.endCol+1]="--"
            
                    
                    
                    
            
    #getting only valid movies
    '''navie algorithm
    1)get the all possible moves
    2)make a each move that are in all possible moves list
    3)check the opps moves for each move we make
    4)if opps moves attack our king then we remove that move from moves list'''
    
    def getValidMoves(self):
        tempempassant=self.empassantMove
        tempcastlerights=CastleRights(self.castelingRights.wks,self.castelingRights.bks,self.castelingRights.wqs,self.castelingRights.bqs)
        moves=self.getAllMoves()
        if(self.whiteToMove):
            self.GetCastleMoves(self.whiteKingLocation[0],self.whiteKingLocation[1],moves)
        else:
            self.GetCastleMoves(self.blackKingLocation[0],self.blackKingLocation[1],moves)
        for i in range(len(moves)-1,-1,-1):
            self.makeMove(moves[i])
            self.whiteToMove= not self.whiteToMove
            if(self.isCheck()):
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undo()
        if(len(moves)==0):
            if(self.isCheck()):
                self.checkMate=True
            else:
                self.staleMate=True
        else:
            self.checkMate=False
            self.staleMate=False
        self.castelingRights=tempcastlerights
        self.empassantMove=tempempassant
        return moves
    def isCheck(self):
        if(self.whiteToMove):
            return self.squareUnderAttack(self.whiteKingLocation[0],self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0],self.blackKingLocation[1])
    def squareUnderAttack(self,r,c):
        self.whiteToMove=not self.whiteToMove
        opps=self.getAllMoves()
        self.whiteToMove=not self.whiteToMove
        for i in opps:
            if(i.endRow==r and i.endCol==c):
                return True
        return False
        
     #getting all moves possible including checks
    def getAllMoves(self):
        moves=[]
        for r in range(8):
            for c in range(8):
                turn =self.board[r][c][0]
                if (turn=="w" and self.whiteToMove) or (turn =="b" and not self.whiteToMove):
                    piece=self.board[r][c][1]
                    self.functions[piece](r,c,moves)
        return moves
        
    #to get pawn moves
    def  getPawnMoves(self,r,c,moves):
        if self.whiteToMove:
            if(self.board[r-1][c]=="--"):# for one move
                moves.append(Move((r,c),(r-1,c),self.board))
            if(r==6 and self.board[r-2][c]=="--"):# for two moves
                moves.append(Move((r,c),(r-2,c),self.board))
            if c-1>=0:
                if(self.board[r-1][c-1][0]=="b"):# to attck enemy piece and to capture left one
                    moves.append(Move((r,c),(r-1,c-1),self.board))
                elif (r-1,c-1)==self.empassantMove:
                    moves.append(Move((r,c),(r-1,c-1),self.board,empassantPossible=True))
                    
            if(c+1<=7):
                if(self.board[r-1][c+1][0]=="b"):#to mcapture right onw
                    moves.append(Move((r,c),(r-1,c+1),self.board))
                elif(r-1,c+1)==self.empassantMove:
                    moves.append(Move((r,c),(r-1,c+1),self.board,empassantPossible=True))
                    
        else:
            if(self.board[r+1][c]=="--"):
                moves.append(Move((r,c),(r+1,c),self.board))
            if(r==1 and self.board[r+2][c]=="--"):
                moves.append(Move((r,c),(r+2,c),self.board))
            if(c-1)>=0:
                if(self.board[r+1][c-1][0]=="w"):#to cAPTURE LEFT One
                    moves.append(Move((r,c),(r+1,c-1),self.board))
                elif (r+1,c-1)==self.empassantMove:
                    moves.append(Move((r,c),(r+1,c-1),self.board,empassantPossible=True))
                    
                    
            if(c+1<=7):
                if(self.board[r+1][c+1][0]=="w"):#to capture right one
                    moves.append(Move((r,c),(r+1,c+1),self.board))
                elif(r+1,c+1)==self.empassantMove :
                    moves.append(Move((r,c),(r+1,c+1),self.board,empassantPossible=True))
                    
            
     #to get rook moves               
    def getRookMoves(self,r,c,moves):
        directions=((-1,0),(0,-1),(1,0),(0,1))#left,down,right,up directions
        if(self.whiteToMove):
            enemy='b'
        else:
            enemy="w"
        for d in directions:
            for i in range(1,8):
                endRow=r+d[0]*i
                endCol=c+d[1]*i
                if(0<=endRow<=7) and (0<=endCol<=7):
                    endpiece=self.board[endRow][endCol]
                    if(endpiece=="--"):
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                    elif(endpiece[0]==enemy):
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                        break
                    else:
                        break
                else:
                    break                   
    #to get knight moves
    def getKnightMoves(self,r,c,moves):
        directions=((-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1))
        ally="w" if self.whiteToMove else "b"
        for d in directions:
            endRow=r+d[0]
            endCol=c+d[1]
            if(0<=endRow<=7) and (0<=endCol<=7):
                endpiece=self.board[endRow][endCol]
                if endpiece[0]!=ally:
                    moves.append(Move((r,c),(endRow,endCol),self.board))
                
                   
            
    #to get bishop moves
    def getBishopMoves(self,r,c,moves):
        directions=((-1,-1),(1,-1),(-1,1),(1,1))#diagonals
        if(self.whiteToMove):#to set enemys
            enemy='b'
        else:
            enemy="w"
        for d in directions:
            for i in range(1,8):
                endRow=r+d[0]*i#calculating next dialong square
                endCol=c+d[1]*i
                if(0<=endRow<=7) and (0<=endCol<=7):
                    endpiece=self.board[endRow][endCol]
                    if(endpiece=="--"):
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                    elif(endpiece[0]==enemy):
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                        break
                    else:
                        break
                else:
                    break
    #to get king moves
    def getKingMoves(self,r,c,moves):
        directions=((1,1),(-1,-1),(0,-1),(0,1),(1,0),(-1,0),(1,-1),(-1,1))
        ally="w" if self.whiteToMove else "b"
        for d in directions:
            endRow=r+d[0]
            endCol=c+d[1]
            if(0<=endRow<=7) and (0<=endCol<=7):
                endpiece=self.board[endRow][endCol]
                if endpiece[0]!=ally:
                    moves.append(Move((r,c),(endRow,endCol),self.board))
            
    def GetCastleMoves(self,r,c,moves):
        if(self.squareUnderAttack(r,c)):
            return #if king under attack there is no castle
        if(self.whiteToMove and self.castelingRights.wks) or (not self.whiteToMove and self.castelingRights.bks):
            self.KingSideCastle(r,c,moves)
        if(self.whiteToMove and self.castelingRights.wqs) or ( not self.whiteToMove and self.castelingRights.bqs):
            self.QueenSideCastle(r,c,moves)
    def KingSideCastle(self,r,c,moves):
        if self.board[r][c+1]=="--" and self.board[r][c+2]=="--":
            if not self.squareUnderAttack(r,c+1) and not self.squareUnderAttack(r,c+2):
                moves.append(Move((r,c),(r,c+2),self.board,isCastle=True))
    def QueenSideCastle(self,r,c,moves):
        if self.board[r][c-1]=="--" and self.board[r][c-2]=="--" and self.board[r][c-3]:
            if not self.squareUnderAttack(r,c-1) and not self.squareUnderAttack(r,c-2):
                moves.append(Move((r,c),(r,c-2),self.board,isCastle=True))
        
        
                
    #to get QUEENS moves
    def getQueenMoves(self,r,c,moves):
        self.getBishopMoves(r,c,moves)
        self.getRookMoves(r,c,moves)
class CastleRights:
    def __init__(self,wks,bks,wqs,bqs):
        self.wks=wks
        self.bks=bks
        self.wqs=wqs
        self.bqs=bqs
class Move:
    #we use chess notation here
    rankstorows={}
    for i in range(8):
        rankstorows[str(i+1)]=8-i-1
    rowstoranks={v:k for k,v in rankstorows.items()}
    filestocols={}
    for i in range(8):
        filestocols[chr(97+i)]=i
    colstofiles={v:k for k,v in filestocols.items()}
    def __init__(self,startSq,endSq,board,empassantPossible=False,isCastle=False):
        self.startRow=startSq[0]
        self.startCol=startSq[1]
        self.endRow=endSq[0]
        self.endCol=endSq[1]
        self.isCastle=isCastle
        self.movedpiece=board[self.startRow][self.startCol]
        self.capturedpiece=board[self.endRow][self.endCol]
        self.moveId=self.startRow*1000+self.startCol*100+self.endRow*10+self.endCol
        self.ispawnpromotion=(self.endRow==0 and self.movedpiece=="wP") or(self.endRow==7 and self.movedpiece=="bP")
        self.isEmpassantMove=(empassantPossible)
        if(self.isEmpassantMove):
            self.capturedpiece="wP" if self.movedpiece=="bP" else "bP"
    #overridiing equal method
    def __eq__(self,other):
        if isinstance(other,Move):
            return self.moveId==other.moveId
        return False
            
    #getting chess notation
    def getChessnotation(self):
        return self.getRankFile(self.startRow,self.startCol)+self.getRankFile(self.endRow,self.endCol)
    def getRankFile(self,r,c):
        return self.colstofiles[c]+self.rowstoranks[r]
