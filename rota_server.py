#creates a UI for the server, which the multiplayer mode of the game relies on 
#finds IP address of computer, asks for which port to run the server on 


import string
import socket
import threading
from queue import Queue
from tkinter import *
####################################
# customize these functions
####################################

def init(data):
    data.port=''
    data.ip=''

def mousePressed(event, data):
    # use event.x and event.y
    if event.x>350 and event.x<550 and event.y>250 and event.y<290:
      if int(data.port)<10000 or int(data.port)>65535:
        data.port=''
      else: 
        HOST = data.ip
        PORT = int(data.port)
        BACKLOG = 50
        #create socket, connect to host, listens and accepts users 
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        server.bind((HOST,PORT))
        server.listen(BACKLOG)
        print("looking for connection")
        
        def handleClient(client, serverChannel, cID, clientele):
          client.setblocking(1)
          msg = ""
          while True:
            try:
              msg += client.recv(10).decode("UTF-8")
              command = msg.split("\n")
              while (len(command) > 1):
                readyMsg = command[0]
                msg = "\n".join(command[1:])
                serverChannel.put(str(cID) + " " + readyMsg)
                command = msg.split("\n")
            except:
              # we failed
              return
        
        def serverThread(clientele, serverChannel):
          while True:
            msg = serverChannel.get(True, None)
            print("msg recv: ", msg)
            msgList = msg.split(" ")
            senderID = int(msgList[0])
            if senderID%2==1:
              intended=senderID+1
            else:
              intended=senderID-1
            instruction = msgList[1]
            details = " ".join(msgList[2:])
            if (details != ""):
              for cID in clientele:
                if cID == intended:
                  #sendMsg = instruction + " " + str(senderID) + " " + details + " " +str(intended) +"\n"
                  sendMsg = instruction + " " + str(senderID) + " " + details + "\n"
                  clientele[cID].send(sendMsg.encode())
                  print("> sent to %s:" % cID, sendMsg[:-1])
            print()
            serverChannel.task_done()
        
        clientele = dict()
        playerNum = 0
        
        serverChannel = Queue(100)
        threading.Thread(target = serverThread, args = (clientele, serverChannel)).start()
        
        names = ["player1", "player2"]
        
        while True:
          try: 
            client, address = server.accept()
            # myID is the key to the client in the clientele dictionary
            myID = playerNum+1
            print(myID, playerNum)
            for cID in clientele:
              print (repr(cID), repr(playerNum))
              clientele[cID].send(("newPlayer %s\n" % myID).encode())
              client.send(("newPlayer %s\n" % cID).encode())
            clientele[myID] = client
            client.send(("myIDis %s \n" % myID).encode())
            print("connection recieved from %s" % myID)
            threading.Thread(target = handleClient, args = 
                                  (client ,serverChannel, myID, clientele)).start()
            playerNum += 1
          except:
            print('max players reached')


def keyPressed(event, data):
    if event.keysym=="BackSpace":
      if len(data.port)!=0:
        data.port=data.port[:-1]
    if len(data.port)<5:
      if event.keysym in string.digits:
        data.port+=event.keysym
    
def redrawAll(canvas, data):
    #citation: geeks for geeks python program to find ip address 
    hostname = socket.gethostname()    
    data.ip = socket.gethostbyname(hostname)
    canvas.create_rectangle(0,0,data.width,data.height,fill='black')
    canvas.create_text(450, 50, text = "Game pin 1: "+str(data.ip), font = "Courier 30", fill = "gray26")
    canvas.create_text(450, 120, text = "Enter game pin 2 below (10000-65535):", font = "Courier 30", fill = "gray26")
    canvas.create_rectangle(350,180,550,220,fill='white')
    canvas.create_text(450,200,text=data.port,font = "Courier 30")
    canvas.create_rectangle(350,250,550,290,fill="gray26")
    canvas.create_text(450,270,text='continue',font="Courier 30", fill='black')
    



####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    root = Tk()
    root.title('server')
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    redrawAll(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(900, 320)

