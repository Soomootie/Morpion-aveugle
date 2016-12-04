import socket
from grid import *




PORT = 7777
HOST = "localhost"
BUFFER = 1500

s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM, proto = 0)
s.connect((HOST,PORT))
player = ""
player = s.recv(1500).decode()

print("Connecté")

grids = [grid(), grid()]
grids[1].display()

if player != "Premier joueur":
    print("En attente ...")
    response = s.recv(BUFFER)
    grids[0].play(2,int(response.decode()))
    
while grids[0].gameOver() == -1: 
    mesg = ''
    shot = -1
    while shot < 0 or shot >= NB_CELLS :
        while shot < 0 or shot >= NB_CELLS :
            mesg = input("Quelle case voulez-vous jouer? [0-8] >> ")
            try:
                shot = int(mesg)
            except ValueError:
                print("Veuillez entrer un entier")
                
            if mesg == 'close':
                s.close()
                break
        if grids[0].cells[shot] != EMPTY:
            print("Coup invalide %d" % shot)
            grids[1].cells[shot] = grids[0].cells[shot]
            grids[0].display()
            shot = -1
        else:  
            grids[0].play(1,shot)
            grids[1].play(1,shot)
            grids[0].display()
            
    s.send(str(shot).encode())

    if grids[0].gameOver() != -1:
        grids[0].printResult()
        break

    print("En attente ...")
    response = s.recv(BUFFER)
    grids[0].play(2,int(response.decode()))
    
    if grids[0].gameOver() != -1:
        grids[0].display()
        grids[0].printResult()
        break

s.close()
print("Socket fermée")