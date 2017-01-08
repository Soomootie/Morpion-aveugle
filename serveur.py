#!/usr/bin/env python3

import socket
import select
import threading

PORT = 7777
BUFFER = 1500

s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM, proto = 0)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
s.bind(('',PORT))
s.listen(1) #ecoute
liste_sockets = []
liste_sockets.append(s)

mesg = ''
reset = 1
while(True):
    (l_rs, l_w, l_e) = select.select(liste_sockets,[],[])

    for i in range(len(l_rs)):
        if l_rs[i] == s:
            (socketx, address) = s.accept() #autorisation de connection
            print("Connection de {}".format(address[1]))
            liste_sockets.append(socketx)
            if len(liste_sockets) == 2:
                print("Premiere connection")
                socketx.send("Premier joueur".encode())
            elif len(liste_sockets) == 3:
                socketx.send("Second joueur".encode())
                liste_sockets[1].send("Second joueur".encode())
                print("Deuxieme connection!")
                if mesg != '':
                    for j in range(len(liste_sockets)):
                        if liste_sockets[j] != s and liste_sockets[j] != l_rs[i]:
                            liste_sockets[j].send(mesg)
                            print("Send :",mesg.decode())
                try:
                    mesg = l_rs[i].recv(BUFFER)
                except OSError:
                    print("OSError")
            else:
                socketx.send("Spectateur".encode())

        elif len(liste_sockets) >= 2:
            try:
                mesg = l_rs[i].recv(BUFFER) #reception des donnees
            except ConnectionResetError:
                print("La connection a été perdue")
                print("Mesg perte connection %s:"%mesg)
                reset = 0
                
            if len(mesg) == 0 or reset == 0:
                liste_sockets.remove(l_rs[i])
                if len(liste_sockets) == 2 :
                    liste_sockets[1].send('Deconnection adversaire'.encode())
                print("Close if longueur")
                l_rs[i].close()
                reset = 1
                mesg = ''
            else:
                print("Mesg :",mesg.decode())
                for j in range(len(liste_sockets)):
                    if liste_sockets[j] != s and liste_sockets[j] != l_rs[i]:
                        print("Avant send mesg %s:"%mesg)
                        liste_sockets[j].send(mesg)
                        print("Send :",mesg.decode())
s.close()
