#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 09:45:38 2020

@author: Tech With Tim
"""
import socket
from _thread import *
import sys
import pickle 
from game import Game

server = socket.gethostname()
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try: 
    s.bind((server, port))
except socket.error as e:
    str(e)
    print(e)
    
s.listen(2)
print("Waiting for a connection, Server started")

connected = set()
games = {}
idCount = 0


def threaded_client(conn, p, gameID):
    global idCount
    conn.send(str.encode(str(p)))
    reply = ""
    while True:
        try:
            #data = conn.recv(4096*8)
            data = conn.recv(4096*32)
            print(data)
            #unserialized_input = pickle.loads(data,encoding='bytes')
            #print(unserialized_input)
            if gameID in games: # if the game still exists
                game = games[gameID]
                if not data:
                    break
                else:
                    if data == 'reset':
                        game.resetWent()
                    elif data != 'get':
                        print("data is not get, playing game")
                        game.play(p, data)
                    
                    reply = game
                    if reply is None:
                        print("dammit... :(")
                    
                    conn.sendall(pickle.dumps(game))
            else:
                break
        except Exception as e:
            print(e)
            break
    
    print("Lost connection")

    try:
        del games[gameID]
        print("Closing game ", gameID)
    except:
        pass
    idCount -= 1
    conn.close()
    
while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)
    idCount += 1
    p = 0
    gameID = (idCount - 1)//2
    if idCount % 2 == 1:
        games[gameID] = Game(gameID)
        print("Creating a new game...")
    else: # both players are connected so they're ready to play
        games[gameID].ready = True
        print("Both players are connected")
        p = 1
        
    start_new_thread(threaded_client, (conn, p, gameID))
