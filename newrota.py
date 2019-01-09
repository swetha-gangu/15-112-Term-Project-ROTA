### Main project code base 
## includes canvas stuff 
## calls from other files to control and draw players/pieces 

from tkinter import*
from image_util import *
from rotaminimax import * 
import math
import socket
import string
import threading
from queue import Queue


    
#######
#Animations 
    
def init(data):
    data.mode='homescreen'
    data.turn='p1'
    data.movingPiece=0
    data.num=None
    data.movesp1=0
    data.movesp2=0
    data.p1=Player1(0)
    data.p2=Player2(0)
    data.me=Player1(0)
    data.other=Player2(0)
    data.IP='172.25.0.95'
    data.PORT=''
    data.isIP=False
    data.isPORT=False
    data.server=None 
    data.serverMsg=Queue(100)
    data.hinting=False
    data.hintmove=None

def mousePressed(event, data):
    if data.mode=='homescreen':
        checkHomeClicks(event,data)
    if data.mode=='playcomp':
        gamePlayer1(event,data)
        if gameStatus.isWinningCombo(data.p1.getpositions())==False:
            gamePlayer2(data)
    if data.mode=='playeasy':
        gamePlayer1(event,data)
        if gameStatus.isWinningCombo(data.p1.getpositions())==False:
            gamePlayer2easy(data)
    if data.mode=='multiplayerstarter':
        if event.x>300 and event.x<600 and event.y>410 and event.y<450:
            data.isIP=True
            data.isPORT=False
        if event.x>300 and event.x<600 and event.y>590 and event.y<630:
            data.isPORT=True 
            data.isIP=False
        if event.x>350 and event.x<550 and event.y>650 and event.y<690:
            try:
                HOST = data.IP
                PORT = int(data.PORT)
                data.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                data.server.connect((HOST,PORT))
                print("connected to server")
                data.mode='multiplayer'
                threading.Thread(target = handleServerMsg, args = (data.server, data.serverMsg)).start()
            except:
                data.mode='multiplayerstarter'
                data.isIP=False
                data.isPORT=False
                data.IP=""
                data.PORT=""
    if data.mode=='multiplayer':
        gamePlayer1(event,data)
        if event.x>50 and event.x<350 and event.y>820 and event.y<870:
            data.hintmove=MaxieMove(data.other,data.me,0,-400000,400000)
            data.hintmove=data.hintmove[0]
            if data.hintmove==None:
                movemade=False
                start=0
                end=0
                if len(data.me.getpositions())<3:
                    for move in range(1,10):
                        if move not in data.other.getpositions() and move not in data.me.getpositions():
                            data.hintmove=(move,0)
                            break
                else:
                    for piece in data.me.getpositions():
                        for move in gameStatus.possiblemoves[piece]:
                            if move not in data.me.getpositions() and move not in data.other.getpositions():
                                start = piece 
                                end = move 
                                data.hintmove=(start,end)
                                movemade=True
                                break
                        if movemade==True:
                            break
            data.hinting=True
    if data.mode=='playcompstarter':
        if event.x>330 and event.x<560 and event.y>500 and event.y<550:
            data.mode='playeasy'
        if event.x>330 and event.x<560 and event.y>600 and event.y<650:
            data.mode='playcomp'
        
        
def handleServerMsg(server, serverMsg):
    server.setblocking(1)
    msg = ""
    command = ""
    while True:
        msg += server.recv(10).decode("UTF-8")
        command = msg.split("\n")
        while (len(command) > 1):
            readyMsg = command[0]
            msg = "\n".join(command[1:])
            serverMsg.put(readyMsg)
            command = msg.split("\n")
        
            
def checkHomeClicks(event,data):
    if event.x>320 and event.x<570 and event.y>380 and event.y<430:
        data.mode='playcompstarter'
    if event.x>320 and event.x<570 and event.y>450 and event.y<500:
        data.mode='multiplayerstarter'
    if event.x>320 and event.x<570 and event.y>520 and event.y<570:
        data.mode='instructions'
    

def keyPressed(event, data):
    if event.keysym=='r':
        init(data)
    if data.mode=='multiplayerstarter':
        if data.isIP==True:
            if event.keysym in string.digits:
                data.IP+=event.keysym
            if event.keysym=='period':
                data.IP+='.'
            if event.keysym=="BackSpace":
                if len(data.IP)>0:
                    data.IP=data.IP[:-1]
        if data.isPORT==True:
            if event.keysym in string.digits:
                data.PORT+=event.keysym
            if event.keysym=="BackSpace":
                if len(data.PORT)>0:
                    data.PORT=data.PORT[:-1]

def drawEmptyRing(canvas,data,cx,cy,r):
    canvas.create_oval(cx-r,cy-r,cx+r,cy+r,fill='gray26')
    canvas.create_oval(cx-r+4,cy-r+4,cx+r-4,cy+r-4,fill='gray11')
    canvas.create_oval(cx-r+6,cy-r+6,cx+r-6,cy+r-6,outline='gray26')
    canvas.create_line(cx,cy-10,cx,cy+10,fill='gray26',width=6)
    canvas.create_line(cx-10,cy,cx+10,cy,fill='gray26',width=6)
    
def drawgameOverPlayer(canvas,data):
    canvas.create_rectangle(0,0,900,900,fill='black')
    canvas.create_rectangle(3*2,3*2,900-3*2,900-3*2,fill='gray4')
    canvas.create_rectangle(3*4,3*4,900-3*4,900-3*4,fill='gray5')
    canvas.create_rectangle(3*6,3*6,900-3*6,900-3*6,fill='gray6')
    canvas.create_rectangle(3*8,3*8,900-3*8,900-3*8,fill='gray7')
    canvas.create_rectangle(3*10,3*10,900-3*10,900-3*10,fill='gray8')
    canvas.create_rectangle(3*12,3*12,900-3*12,900-3*12,fill='gray9')
    canvas.create_rectangle(3*14,3*14,900-3*14,900-3*14,fill='gray10')
    canvas.create_rectangle(3*16,3*16,900-3*16,900-3*16,fill='gray11')
    canvas.create_rectangle(3*30,3*30,900-3*30,900-3*30,fill='gray26')
    canvas.create_rectangle(3*32,3*32,900-3*32,900-3*32,fill='gray11')
    canvas.create_oval(150,150,750,750,outline='gray26',width=6)
    centx, centy = 450, 450
    gap=360//8
    angle=0
    r=300
    for i in range(8):
        ex=centx+r*math.cos(math.radians(angle))
        ey=centy+r*math.sin(math.radians(angle))
        drawEmptyRing(canvas,data,ex,ey,40)
        angle+=gap
    canvas.create_text(450, 370, text = "GAME OVER", font = "Courier 60", fill = "gray26")
    canvas.create_text(450, 470, text = "You won!", font = "Courier 50", fill = "gray26")
    canvas.create_text(450,550, text = str(data.movesp1)+" moves", font = "Courier 40", fill = "gray26")
    
    
def drawgameOverComp(canvas,data):
    canvas.create_rectangle(0,0,900,900,fill='black')
    canvas.create_rectangle(3*2,3*2,900-3*2,900-3*2,fill='gray4')
    canvas.create_rectangle(3*4,3*4,900-3*4,900-3*4,fill='gray5')
    canvas.create_rectangle(3*6,3*6,900-3*6,900-3*6,fill='gray6')
    canvas.create_rectangle(3*8,3*8,900-3*8,900-3*8,fill='gray7')
    canvas.create_rectangle(3*10,3*10,900-3*10,900-3*10,fill='gray8')
    canvas.create_rectangle(3*12,3*12,900-3*12,900-3*12,fill='gray9')
    canvas.create_rectangle(3*14,3*14,900-3*14,900-3*14,fill='gray10')
    canvas.create_rectangle(3*16,3*16,900-3*16,900-3*16,fill='gray11')
    canvas.create_rectangle(3*30,3*30,900-3*30,900-3*30,fill='gray26')
    canvas.create_rectangle(3*32,3*32,900-3*32,900-3*32,fill='gray11')
    canvas.create_oval(150,150,750,750,outline='gray26',width=6)
    centx, centy = 450, 450
    gap=360//8
    angle=0
    r=300
    for i in range(8):
        ex=centx+r*math.cos(math.radians(angle))
        ey=centy+r*math.sin(math.radians(angle))
        drawEmptyRing(canvas,data,ex,ey,40)
        angle+=gap
    canvas.create_text(450, 370, text = "GAME OVER", font = "Courier 60", fill = "gray26")
    canvas.create_text(450, 470, text = "You lost :(", font = "Courier 50", fill = "gray26")
    canvas.create_text(450,550, text = str(data.movesp1)+" moves", font = "Courier 40", fill = "gray26")
    
def drawBoard(canvas,data):
    canvas.create_rectangle(0,0,900,900,fill='black')
    canvas.create_rectangle(3*2,3*2,900-3*2,900-3*2,fill='gray4')
    canvas.create_rectangle(3*4,3*4,900-3*4,900-3*4,fill='gray5')
    canvas.create_rectangle(3*6,3*6,900-3*6,900-3*6,fill='gray6')
    canvas.create_rectangle(3*8,3*8,900-3*8,900-3*8,fill='gray7')
    canvas.create_rectangle(3*10,3*10,900-3*10,900-3*10,fill='gray8')
    canvas.create_rectangle(3*12,3*12,900-3*12,900-3*12,fill='gray9')
    canvas.create_rectangle(3*14,3*14,900-3*14,900-3*14,fill='gray10')
    canvas.create_rectangle(3*16,3*16,900-3*16,900-3*16,fill='gray11')
    canvas.create_rectangle(3*30,3*30,900-3*30,900-3*30,fill='gray26')
    canvas.create_rectangle(3*32,3*32,900-3*32,900-3*32,fill='gray11')
    canvas.create_oval(150,150,750,750,outline='gray26',width=6)
    centx, centy = 450, 450
    gap=360//8
    angle=0
    r=300
    for i in range(8):
        ex=centx+r*math.cos(math.radians(angle))
        ey=centy+r*math.sin(math.radians(angle))
        canvas.create_line(centx,centy,ex,ey,fill='gray26',width=6)
        drawEmptyRing(canvas,data,ex,ey,40)
        angle+=gap
    #middle ring
    drawEmptyRing(canvas,data,centx,centy,40)
    
def drawTurn(canvas,data):
    if data.turn=='p1':
        canvas.create_rectangle(350,55,550,85,fill='#a88741')
    if data.turn=='p2':
        canvas.create_rectangle(350,55,550,85,fill='#403c96')
    canvas.create_text(800, 55, text = "moves: "+str(data.movesp1), font = "Courier 20", fill = '#a88741')
    canvas.create_text(100, 55, text = "moves: "+str(data.movesp2), font = "Courier 20", fill = '#403c96')
    
    
def drawMultiplayerStarter(canvas,data):
    canvas.create_rectangle(0,0,900,900,fill='black')
    canvas.create_rectangle(3*2,3*2,900-3*2,900-3*2,fill='gray4')
    canvas.create_rectangle(3*4,3*4,900-3*4,900-3*4,fill='gray5')
    canvas.create_rectangle(3*6,3*6,900-3*6,900-3*6,fill='gray6')
    canvas.create_rectangle(3*8,3*8,900-3*8,900-3*8,fill='gray7')
    canvas.create_rectangle(3*10,3*10,900-3*10,900-3*10,fill='gray8')
    canvas.create_rectangle(3*12,3*12,900-3*12,900-3*12,fill='gray9')
    canvas.create_rectangle(3*14,3*14,900-3*14,900-3*14,fill='gray10')
    canvas.create_rectangle(3*16,3*16,900-3*16,900-3*16,fill='gray11')
    canvas.create_rectangle(3*30,3*30,900-3*30,900-3*30,fill='gray26')
    canvas.create_rectangle(3*32,3*32,900-3*32,900-3*32,fill='gray11')
    canvas.create_oval(150,150,750,750,outline='gray26',width=6)
    centx, centy = 450, 450
    gap=360//8
    angle=0
    r=300
    for i in range(8):
        ex=centx+r*math.cos(math.radians(angle))
        ey=centy+r*math.sin(math.radians(angle))
        drawEmptyRing(canvas,data,ex,ey,40)
        angle+=gap
    canvas.create_text(450, 370, text = "Enter game pin 1:", font = "Courier 40", fill = "gray26")
    canvas.create_rectangle(300,410,600,450,fill='white')
    canvas.create_text(450,430,text=data.IP)
    canvas.create_text(450,550, text = "Enter game pin 2:", font = "Courier 40", fill = "gray26")
    canvas.create_rectangle(300,590,600,630,fill='white')
    canvas.create_text(450,610,text=data.PORT)
    canvas.create_rectangle(350,650,550,690,fill="gray26")
    canvas.create_text(450,670,text='continue',font="Courier 40", fill='black')
    
    
def drawHomeScreen(canvas,data):
    canvas.create_rectangle(0,0,900,900,fill='black')
    canvas.create_rectangle(3*2,3*2,900-3*2,900-3*2,fill='gray4')
    canvas.create_rectangle(3*4,3*4,900-3*4,900-3*4,fill='gray5')
    canvas.create_rectangle(3*6,3*6,900-3*6,900-3*6,fill='gray6')
    canvas.create_rectangle(3*8,3*8,900-3*8,900-3*8,fill='gray7')
    canvas.create_rectangle(3*10,3*10,900-3*10,900-3*10,fill='gray8')
    canvas.create_rectangle(3*12,3*12,900-3*12,900-3*12,fill='gray9')
    canvas.create_rectangle(3*14,3*14,900-3*14,900-3*14,fill='gray10')
    canvas.create_rectangle(3*16,3*16,900-3*16,900-3*16,fill='gray11')
    canvas.create_rectangle(3*30,3*30,900-3*30,900-3*30,fill='gray26')
    canvas.create_rectangle(3*32,3*32,900-3*32,900-3*32,fill='gray11')
    canvas.create_oval(150,150,750,750,outline='gray26',width=6)
    centx, centy = 450, 450
    gap=360//8
    angle=0
    r=300
    for i in range(8):
        ex=centx+r*math.cos(math.radians(angle))
        ey=centy+r*math.sin(math.radians(angle))
        drawEmptyRing(canvas,data,ex,ey,40)
        angle+=gap
    canvas.create_text(450, 300, text = "R O T A", font = "Courier 70", fill = "gray26")
    createButton(canvas,320,380,'play computer')
    createButton(canvas,320,450,'play multiplayer')
    createButton(canvas,320,520,'instructions')
    
def gamePlayer1(event,data):
    if gameStatus.isWinningCombo(data.p2.getpositions())==True:
        data.mode='gameovercomp'
    if data.turn=='p1':
        if data.mode=='multiplayer':
            msg = ""
            data.num=Pieces.getPiecePosition(event.x,event.y)
            if data.num!=None:
                if data.num !=None and data.num not in data.me.getpositions() and data.num not in data.other.getpositions() and data.me.getnumPieces()<3:
                    data.me.addPiece(data.num)
                    data.movesp1+=1
                    data.turn='p2'
                    data.hinting=False
                    msg = "move %d %d\n" % (data.num, 0)
                elif data.num!=None and data.num in data.me.getpositions() and data.movingPiece==0:
                    data.movingPiece=data.num
                elif data.num!=None and data.movingPiece!=0:
                    data.me.movePiece(data.movingPiece,data.num)
                    msg = "move %d %d\n" % (data.movingPiece, data.num)
                    data.movingPiece=0
                    data.hinting=False
                    data.turn='p2'
                    data.movesp1+=1
                if (msg != ""):
                    print ("sending: ", msg,)
                    data.server.send(msg.encode())
            if gameStatus.isWinningCombo(data.me.getpositions())==True:
                data.mode='gameoverplayer'
            
        else:
            data.num=Pieces.getPiecePosition(event.x,event.y)
            if data.num !=None and data.num not in data.p1.getpositions() and data.num not in data.p2.getpositions() and data.p1.getnumPieces()<3:
                data.p1.addPiece(data.num)
                data.movesp1+=1
                data.turn='p2'
                msg = "move %d %d\n" % (data.num, 0)
            elif data.num!=None and data.num in data.p1.getpositions() and data.movingPiece==0:
                data.movingPiece=data.num
            elif data.num!=None and data.movingPiece!=0:
                data.p1.movePiece(data.movingPiece,data.num)
                msg = "move %d %d\n" % (data.movingPiece, data.num)
                data.movingPiece=0
                data.turn='p2'
                data.movesp1+=1
            if gameStatus.isWinningCombo(data.p1.getpositions())==True:
                data.mode='gameoverplayer'
        
def gamePlayer2(data):
    if data.turn=='p2':
        nextMove=MaxieMove(data.p1,data.p2,0,-300*3*300,300*3*300)
        if nextMove[0]==None:
            print('not working') 
            movemade=False
            start=0
            end=0
            if len(data.p2.getpositions())<3:
                for move in range(1,10):
                    if move not in data.p1.getpositions() and move not in data.p2.getpositions():
                        start = move
                        data.p2.movePiece(start,end)
                        break
            else:
                for piece in data.p2.getpositions():
                    for move in gameStatus.possiblemoves[piece]:
                        if move not in data.p1.getpositions() and move not in data.p2.getpositions():
                            start = piece 
                            end = move 
                            data.p2.movePiece(start,end)
                            movemade=True
                            break
                    if movemade==True:
                        break
        else:
            data.p2.movePiece(nextMove[0][0],nextMove[0][1])
            data.movesp2+=1
        data.turn='p1'
        if gameStatus.isWinningCombo(data.p2.getpositions())==True:
            data.mode='gameovercomp'
            
            
def gamePlayer2easy(data):
    if data.turn=='p2':
        movemade=False
        start=0
        end=0
        if len(data.p2.getpositions())<3:
            for move in range(1,10):
                if move not in data.p1.getpositions() and move not in data.p2.getpositions():
                    start = move
                    data.p2.movePiece(start,end)
                    break
        else:
            for piece in data.p2.getpositions():
                for move in gameStatus.possiblemoves[piece]:
                    if move not in data.p1.getpositions() and move not in data.p2.getpositions():
                        start = piece 
                        end = move 
                        data.p2.movePiece(start,end)
                        movemade=True
                        break
                if movemade==True:
                    break
        data.movesp2+=1
        data.turn='p1'
        if gameStatus.isWinningCombo(data.p2.getpositions())==True:
            data.mode='gameovercomp'
        
def timerFired(data):
    # timerFired receives instructions and executes them
    if data.mode=='multiplayer':
        if data.serverMsg!=None:
            while (data.serverMsg.qsize() > 0):
                msg = data.serverMsg.get(False)
            
                print("received: ", msg, "\n")
                msg = msg.split()
                command = msg[0]
                if (command == "newPlayer"):
                    if int(data.me.getPID())%2==1:
                        if int(msg[1])==data.me.getPID()+1:
                            newPID=int(msg[1])
                            data.other=Player2(newPID)
                    else:
                        if int(msg[1])==data.me.getPID()-1:
                            newPID=int(msg[1])
                            data.other=Player2(newPID)
                if (command == "myIDis"):
                    myPID = int(msg[1])
                    data.me.changePID(myPID)
                if (command == 'move'):
                    #if msg[4]==data.me.getPID():
                    data.other.movePiece(int(msg[2]),int(msg[3]))
                    data.movesp2+=1
                    data.turn='p1'
                    if gameStatus.isWinningCombo(data.other.getpositions())==True:
                        data.mode='gameovercomp'
                # except:
                #     print("failed")
                data.serverMsg.task_done()

def drawPlayCompStarter(canvas,data):
    canvas.create_rectangle(0,0,900,900,fill='black')
    canvas.create_rectangle(3*2,3*2,900-3*2,900-3*2,fill='gray4')
    canvas.create_rectangle(3*4,3*4,900-3*4,900-3*4,fill='gray5')
    canvas.create_rectangle(3*6,3*6,900-3*6,900-3*6,fill='gray6')
    canvas.create_rectangle(3*8,3*8,900-3*8,900-3*8,fill='gray7')
    canvas.create_rectangle(3*10,3*10,900-3*10,900-3*10,fill='gray8')
    canvas.create_rectangle(3*12,3*12,900-3*12,900-3*12,fill='gray9')
    canvas.create_rectangle(3*14,3*14,900-3*14,900-3*14,fill='gray10')
    canvas.create_rectangle(3*16,3*16,900-3*16,900-3*16,fill='gray11')
    canvas.create_rectangle(3*30,3*30,900-3*30,900-3*30,fill='gray26')
    canvas.create_rectangle(3*32,3*32,900-3*32,900-3*32,fill='gray11')
    canvas.create_oval(150,150,750,750,outline='gray26',width=6)
    centx, centy = 450, 450
    gap=360//8
    angle=0
    r=300
    for i in range(8):
        ex=centx+r*math.cos(math.radians(angle))
        ey=centy+r*math.sin(math.radians(angle))
        drawEmptyRing(canvas,data,ex,ey,40)
        angle+=gap
    canvas.create_text(450, 400, text = "R O T A", font = "Courier 70", fill = "gray26")
    createButton(canvas,330,500,'play easy')
    createButton(canvas,330,600,'play hard')
    
def createButton(canvas,topx,topy,text):
    canvas.create_rectangle(topx,topy,topx+270,topy+50,outline='gray11')
    canvas.create_rectangle(topx+4,topy+4,topx+266,topy+46,outline='gray26',width=4)
    canvas.create_rectangle(topx+6,topy+6,topx+264,topy+44,fill='gray11')
    canvas.create_text((2*topx+100)//2,topy+16,text=text,fill='gray26',anchor=NW,font="Courier 20 italic")
    
def redrawAll(canvas, data):
    if data.mode=='homescreen':
        drawHomeScreen(canvas,data)
    if data.mode=='playcomp':
        drawBoard(canvas,data)
        data.p1.drawPlayer1(canvas)
        data.p2.drawPlayer2(canvas)
        drawTurn(canvas,data)
    if data.mode=='playeasy':
        drawBoard(canvas,data)
        data.p1.drawPlayer1(canvas)
        data.p2.drawPlayer2(canvas)
        drawTurn(canvas,data)
    if data.mode=='multiplayer':
        drawBoard(canvas,data)
        data.me.drawPlayer1(canvas)
        canvas.create_text(760, 140, text=str(data.me.getPID()), fill='gray26', font="Courier 30 italic")
        data.other.drawPlayer2(canvas)
        drawTurn(canvas,data)
        canvas.create_text(200,830,text='need a hint?',fill='gray26',font="Courier 40 italic")
        if data.hinting==True:
            gap=360//8
            angle=0
            r=350
            for i in range(1,9):
                ex=450+r*math.cos(math.radians(angle))
                ey=450+r*math.sin(math.radians(angle))
                canvas.create_text(ex,ey,text=str(i), fill='#a88741',font="Courier 40 italic")
                angle-=gap
            canvas.create_text(450,400,text='9', fill='#a88741',font="Courier 40 italic")
            if data.hintmove[1]==0:
                canvas.create_text(600,830,text='place a piece on '+str(data.hintmove[0]), fill='#a88741',font="Courier 40 italic")
            if data.hintmove[1]!=0:
                canvas.create_text(600,830,text='move from '+str(data.hintmove[0])+' to '+str(data.hintmove[1]), fill='#a88741',font="Courier 40 italic")
    if data.mode=='multiplayerstarter':
        drawMultiplayerStarter(canvas,data)
    if data.mode=='instructions':
        instructions=PhotoImage(file="instructions.png") 
        canvas.create_image(0, 0, anchor=NW, image=instructions)
        label=Label(image=instructions)
        label.image = instructions
    if data.mode=='gameovercomp':
        drawgameOverComp(canvas,data)
    if data.mode=='gameoverplayer':
        drawgameOverPlayer(canvas,data)
    if data.mode=='playcompstarter':
        drawPlayCompStarter(canvas,data)
    

####################################
# use the run function as-is
####################################
#def run(width, height, serverMsg=None, server=None):
def run(width, height):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    #data.server = server
    #data.serverMsg = serverMsg
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    root.title('ROTA')
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)

        #data.serverMsg = Queue(100)
        #threading.Thread(target = handleServerMsg, args = (data.server, data.serverMsg)).start()
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")



run(900, 900)

