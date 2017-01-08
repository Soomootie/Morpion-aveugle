import socket
from grid import *
from optparse import OptionParser
import os,platform
from docopt import docopt

if platform.system() == "Linux":
    os.system("clear")
else:
    os.system("cls")


help = """Client_morpion_aveugle
 
Usage:
  client.py [<serveur>]
 
"""
 
arguments = docopt(help)
print(arguments['<serveur>'])

PORT = 7777
HOST = arguments['<serveur>']
BUFFER = 1024

FIRST = "Premier joueur"
SECOND = "Second joueur"
DISCO = "Deconnection adversaire"

s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM, proto = 0)
s.connect((HOST,PORT))

player = ""
player = s.recv(BUFFER).decode()

grids = [grid(), grid()]
grids[1].display()

if player == FIRST:
    print("En attente d'un second joueur...")
    response = s.recv(BUFFER).decode()
    while response != SECOND:
        response = s.recv(BUFFER).decode()
if player == SECOND:
    response = s.recv(BUFFER).decode()
    while response == DISCO or response == SECOND:
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
            grids[1].display()
            shot = -1
        else:  
            grids[0].play(1,shot)
            grids[1].play(1,shot)
            grids[0].display()
            
    s.send(str(shot).encode())

    if grids[0].gameOver() != -1:
        grids[0].printResult()
        break

    
    try:
        print("Le second joueur reflechi...")
        response = s.recv(BUFFER).decode()
        response = response[0:len(DISCO)]
    except ConnectionAbortedError:
        print("Votre adversaire est parti !")
        response = DISCO
    if response != DISCO:
        if response != '':
            response = response[len(response)-1]
        if response != '' and response.isdigit():
            grids[0].play(2,int(response))
    else:
        while response == DISCO:
            try:
                response = s.recv(BUFFER).decode()
            except ConnectionAbortedError:                
                response = DISCO
            
        print("OOPS, votre adversaire est parti !")

        grids = [grid(), grid()]
        grids[0].play(1,shot)
        grids[1].play(1,shot)
        if response != '' and response.isdigit():
            grids[0].play(2,int(response))

    if grids[0].gameOver() != -1:
        grids[0].display()
        grids[0].printResult()
        break

s.close()
print("Socket fermée")
