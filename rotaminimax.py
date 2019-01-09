import math
import copy

#### AI; minimax algorithm; controls Player2 in hard play computer mode 

def heuristicHelper(p):
    if len(p)==2:
        a=Pieces.getPieceCoordinates(p[0])
        b=Pieces.getPieceCoordinates(p[1])
        dab=math.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)
        return dab
    elif len(p)==3: 
        a=Pieces.getPieceCoordinates(p[0])
        b=Pieces.getPieceCoordinates(p[1])
        c=Pieces.getPieceCoordinates(p[2])
        dab=math.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)
        dac=math.sqrt((a[0]-c[0])**2+(a[1]-c[1])**2)
        dbc=math.sqrt((c[0]-b[0])**2+(c[1]-b[1])**2)
        s=(dab+dac+dbc)/2
        area=math.sqrt(s*(s-dab)*(s-dac)*(s-dbc))
        return area
    else:
        return 0
        
def heuristic(p1,p2):
    heurp1=heuristicHelper(p1)
    heurp2=heuristicHelper(p2)
    if heurp1<=200:
        return float('-inf')
    elif heurp2<=200: 
        return float('inf')
    return heurp1-heurp2

    
    
def MaxieMove(p1,p2,depth,alpha,beta):
    assert(alpha<beta)
    if gameStatus.gameComplete(p1.getpositions(),p2.getpositions())!=None:
        if gameStatus.gameComplete(p1.getpositions(),p2.getpositions())=='p2':
            return (None, float('inf'))
        else: 
            return (None, float('-inf'))
    elif depth==4:
        return (None, heuristic(p1.getpositions(),p2.getpositions()))
    else:
        bestMove = None
        bestScore = float('-inf')
        if p2.getnumPieces()<3:
            for move in range(1,10):
                if move not in p1.getpositions() and move not in p2.getpositions():
                    p2.movePiece(move,0)
                    minMove, moveScore=MinnieMove(p1,p2,depth,alpha,beta)
                    p2.removePiece(move)
                    if moveScore>bestScore:
                        bestScore=moveScore
                        bestMove=(move,0)
                        alpha = max(alpha, bestScore)
                        if (alpha >= beta):
                            return (bestMove, bestScore) 
        else: 
            for piece in p2.getpositions():
                for move in gameStatus.getpossibleMoves()[piece]:
                    if move not in p1.getpositions() and move not in p2.getpositions():
                        p2.movePiece(piece,move)
                        minMove, moveScore=MinnieMove(p1,p2,depth,alpha,beta)
                        p2.movePieceback(piece,move)
                        if moveScore>bestScore:
                            bestScore=moveScore
                            bestMove=(piece,move)
                            alpha = max(alpha, bestScore)
                            if (alpha >= beta):
                                return (bestMove, bestScore)
        return (bestMove, bestScore)
                    

# same as Maxie, but maximizes Minnie's score by minimizing
# the board score
def MinnieMove(p1,p2,depth,alpha,beta):
    assert(alpha < beta)
    if gameStatus.gameComplete(p1.getpositions(),p2.getpositions())!=None:
        if gameStatus.gameComplete(p1.getpositions(),p2.getpositions())=='p1':
            return (None, float('-inf'))
        else: 
            return (None, float('inf'))
    elif depth==4:
        return (None, heuristic(p1.getpositions(),p2.getpositions()))
    else:
        bestMove = None
        bestScore = float('inf')
        if p1.getnumPieces()<3:
            for move in range(1,10):
                if move not in p1.getpositions() and move not in p2.getpositions():
                    p1.movePiece(move,0)
                    minMove, moveScore=MaxieMove(p1,p2,depth+1,alpha,beta)
                    p1.removePiece(move)
                    if moveScore<bestScore:
                        bestScore=moveScore
                        bestMove=(move,0)
                        beta = min(beta, bestScore)
                        if (alpha >= beta):
                            return (bestMove, bestScore)
        else: 
            for piece in p1.getpositions():
                for move in gameStatus.getpossibleMoves()[piece]:
                    if move not in p1.getpositions() and move not in p2.getpositions():
                        p1.movePiece(piece,move)
                        maxMove, moveScore=MaxieMove(p1,p2,depth+1,alpha,beta)
                        p1.movePieceback(piece,move)
                        if moveScore<bestScore:
                            bestScore=moveScore
                            bestMove=(piece,move)
                            beta = min(beta, bestScore)
                            if (alpha >= beta):
                                return (bestMove, bestScore)
        return (bestMove, bestScore)


# Creates the player objects 
####
#Player classes 

class Player(object):
    #Model
    def __init__(self,PID,positions=None):
        if positions==None:
            self.numPieces=0
        else:
            self.numPieces = len(positions)
        if positions==None:
            self.positions=[]
        else:
            self.positions=positions
        self.numMoves=0
        self.PID=PID
    
    def getpositions(self):
        return copy.deepcopy(self.positions)
        
    def getnumPieces(self):
        return self.numPieces
        
    def getnumMoves(self):
        return str(self.numMoves)
        
    def changePID(self,PID):
        self.PID=PID
        
    def getPID(self):
        return self.PID
        
    def addPiece(self,piece):
        self.movePiece(piece)
            
    def removePiece(self,place):
        self.numPieces-=1
        self.positions.remove(place)
    
    def movePiece(self,start,end=0):
        if self.numPieces<3:
            if end==0:
                self.numPieces+=1
                self.numMoves+=1
                self.positions.append(start)
        if end!=0:
            if gameStatus.canMove(start,end)==True:
                self.positions.remove(start)
                self.numMoves+=1
                self.positions.append(end)
            
    def movePieceback(self,start,end):
        self.positions.append(start)
        self.positions.remove(end)
        
class Player1(Player):
    def drawPlayer1(self,canvas):
        for i in self.positions:
            Pieces.drawPiece(canvas,i,'#a88741')
        
class Player2(Player):
    def drawPlayer2(self,canvas):
        for i in self.positions:
            Pieces.drawPiece(canvas,i,'#403c96')




####
#Helpful methods for pieces + positions 
# helps find coordinates for pieces and tells what clicks are for what piece 

class Pieces(object):
    @staticmethod
    def getPiecePosition(x,y):
        if x>(450-40) and x<(450+40) and y>(450-40) and y<(450+40):
            return 9
        if x>(750-40) and x<(750+40) and y>(450-40) and y<(450+40):
            return 1
        if x>(662.132-40) and x<(662.132+40) and y>(237.86797-40) and y<(237.86797+40):
            return 2
        if x>(450-40) and x<(450+40) and y>(150-40) and y<(150+40):
            return 3
        if x>(237.86797-40) and x<(237.86797+40) and y>(237.86797-40) and y<(237.86797+40):
            return 4
        if x>(150-40) and x<(150+40) and y>(450-40) and y<(450+40):
            return 5
        if x>(237.86797-40) and x<(237.86797+40) and y>(662.132-40) and y<(662.132+40):
            return 6
        if x>(450-40) and x<(450+40) and y>(750-40) and y<(750+40):
            return 7
        if x>(662.132-40) and x<(662.132+40) and y>(662.132-40) and y<(662.132+40):
            return 8
        return None 
    
    @staticmethod
    def getPieceCoordinates(num):
        if num>9 or num <1:
            return None 
        if num==9: 
            return (450,450)
        if num==1:
            return(750,450)
        if num==2:
            return(662.132,237.86797)
        if num==3:
            return(450,150)
        if num==4:
            return(237.86797,237.86797)
        if num==5:
            return(150,450)
        if num==6:
            return(237.86797,662.132)
        if num==7:
            return(450,750)
        if num==8:
            return(662.132,662.132)
    
    @staticmethod
    def drawPiece(canvas,num,color):
        if num!=None and num!=0:
            cx,cy=Pieces.getPieceCoordinates(num)
            canvas.create_oval(cx-37,cy-37,cx+37,cy+37,fill=color)
            
            
# allows other files to check what moves are legal and when the game is over 

####
class gameStatus(object):
    
    possiblemoves={1:{2,8,9},2:{1,9,3},3:{4,9,2},4:{3,9,5},5:{4,9,6},6:{5,9,7},7:{6,9,8},8:{1,9,7},9:{1,2,3,4,5,6,7,8}}
    
    @staticmethod
    def getpossibleMoves():
        return gameStatus.possiblemoves
    
    # @staticmethod
    # def canMove(start, end, p1,p2):
    #     if end not in possiblemoves[start]:
    #         return False 
    #     if end in p1.positions() or end in p2.positions():
    #         return False 
    #     return True 
    
    @staticmethod
    def canMove(start, end):
        if end not in gameStatus.possiblemoves[start]:
            return False 
        return True 
    
    winningCombos=[[3,9,7],[2,9,6],[1,9,5],[8,9,4],[1,2,3],[2,3,4],[3,4,5],[4,5,6],[5,6,7],[6,7,8],[8,1,2],[1,8,7]]
    setwinningCombos={1:{3,9,7},2:{2,9,6},3:{1,9,5},4:{8,9,4},5:{1,2,3},6:{2,3,4},7:{3,4,5},8:{4,5,6},9:{5,6,7},10:{6,7,8},11:{8,1,2},12:{1,8,7}}
    
    def isWinningCombo(lst):
        if len(lst)<3:
            return False
        pieces=set(lst)
        for combo in gameStatus.setwinningCombos.values():
            if gameStatus.inHere(pieces,combo)==True:
                return True 
        return False 
    
    def inHere(pieces,st):
        for piece in pieces:
            if piece not in st:
                return False
        return True 
    
    
    @staticmethod
    def gameComplete(p1,p2):
        if gameStatus.isWinningCombo(p1)==True:
            return 'p1'
        elif gameStatus.isWinningCombo(p2)==True:
            return 'p2'
        else:
            return None 
