import socket
from grid import *

import os,platform

if platform.system() == "Linux":
    os.system("clear")
else:
    os.system("cls")

PORT = 7777
HOST = "localhost"
BUFFER = 1024

s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM, proto = 0)
s.connect((HOST,PORT))

player = ""
player = s.recv(BUFFER).decode()

print("Connecté")

grids = [grid(), grid()]
grids[1].display()

if player != "Premier joueur":
    print("En attente ...")
    response = s.recv(BUFFER).decode()
    while response == "Deconnection adversaire":
        response = s.recv(BUFFER).decode()
    grids[0].play(2,int(response))
    
while grids[0].gameOver() == -1: 
    # mesg = ''
    shot = -1
    while shot < 0 or shot >= NB_CELLS :
        while shot < 0 or shot >= NB_CELLS :
            mesg = input("Quelle case voulez-vous jouer? [0-8] >> ")
            try:
                shot = int(mesg)
            except ValueError:
                print("Veuillez entrer un entier !")

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
    response = s.recv(BUFFER).decode()
    if response != 'Deconnection adversaire':
        grids[0].play(2,int(response))
    else:
        while response == "Deconnection adversaire":
            response = s.recv(BUFFER).decode()
        print("OOPS, votre adversaire est parti !")
        
        grids = [grid(), grid()]
    if grids[0].gameOver() != -1:
        grids[0].display()
        grids[0].printResult()
        break

s.close()
print("Socket fermée")
