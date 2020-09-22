#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 11:20:41 2020

@author: jferina
"""

import socket
import time
import pickle
import numpy as np


HEADERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((socket.gethostname(), 1235))
s.listen(5)

while True:
    # now our endpoint knows about the OTHER endpoint.
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established.")
    
    d = np.random.randint(low = 0, high = 255, size = (1200,1200,4))
    msg = pickle.dumps(d)
    msg = bytes(f'{len(msg):<{HEADERSIZE}}','utf-8') + msg

    # msg = "Welcome to the server!"
    # msg = f"{len(msg):<{HEADERSIZE}}"+msg

    clientsocket.send(msg)
