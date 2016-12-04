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

while(True):
    (l_rs, l_w, l_e) = select.select(liste_sockets,[],[])
    for i in range(len(l_rs)):
        if l_rs[i] == s:
            print(len(liste_sockets))
            (socketx, address) = s.accept() #authorisation de connection
            print("Connection de {}".format(address[0]))
            liste_sockets.append(socketx)
            print(len(liste_sockets))
            if len(liste_sockets) == 2:
                socketx.send("Premier joueur".encode())
            else:
                socketx.send("Second joueur".encode())
        else:
            mesg = l_rs[i].recv(BUFFER) #reception des donnees
            print("Mesg :",mesg.decode())
            if len(mesg) == 0:
                liste_sockets.remove(l_rs[i])
                print("Close")
                l_rs[i].close()
            else:
                for j in range(len(liste_sockets)):
                    if liste_sockets[j] != s and liste_sockets[j] != l_rs[i]:
                        liste_sockets[j].send(mesg)
                        print("Send :",mesg.decode())
s.close()
