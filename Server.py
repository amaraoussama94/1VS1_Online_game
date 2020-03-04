# Server
# windows test
import socket
from _thread import *
import pickle
from game import Game

# via cmd -> ipconfig ->IPV4
server = '192.168.43.73'  # "IP" you wil gett an error: use 'IP'
port = 5555  # open port

connected=set() # store ip add of the connected client
games={}
idCount= 0

def threaded_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p))) # p0 or p1
    reply=""
    while True :
        try :
            data =conn.recv(4096).decode()
            # check if  someone disconnect then   delete the gameId
            if gameId in games :
                game = games[gameId]
                if  not data:
                    break
                else :
                    if data =="reset":
                        game.resetWin()
                    elif data != "get":
                        game.player(p,data)
                    reply =game
                    conn.sendall(pickle.dumps(reply))
            else :
                print("error")
                break
        except :
            print(" error no data recv")
            break
    print ("lost connection")

    try:
        del games[gameId]
        print("closing Game", gameId)
    except:
        print("can t del games[gameId]" )
        pass
    idCount-=1
    conn.close()

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # type of  connection

try:

    serversocket.bind((server, port))

except  socket.error as e:
    print(str(e))

# max_conn =2
serversocket.listen(2)  # open the port 2 pp  only can connect to the port
print("waiting for connection , Server Sttarted")

while True:
    (conn, addr) = serversocket.accept()  # accept any connection and sotre the connection and IP adress
    print("connected to :  ", addr)

    idCount += 1 # to see how many pp connected to th sever
    p=0 # player  1
    gameId = (idCount -1)//2  # for  every 2 pp increment  by 1
    if (idCount % 2)==1:
        games[gameId]=Game(gameId) # add new game for this player
        print("creating new game ...")
    else:
        games[gameId].ready = True # there is 2 player connected start new game
        p=1

    start_new_thread(threaded_client, (conn,p, gameId ))





