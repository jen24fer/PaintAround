#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 11:25:26 2020

@author: jferina
"""

import socket
import pickle
import matplotlib.pyplot as plt

HEADERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 1235))
msglen = HEADERSIZE
while True:
    full_msg = b''
    new_msg = True
    while True:
        msg = s.recv(msglen)
        if new_msg:
            print("new msg len:",msg[:HEADERSIZE])
            msglen = int(msg[:HEADERSIZE])
            new_msg = False

        print(f"full message length: {msglen}")

        full_msg += msg

        print(len(full_msg))


        if len(full_msg)-HEADERSIZE == msglen:
            print("full msg recvd")
            d = pickle.loads(full_msg[HEADERSIZE:])
            print(d)
            plt.imshow(d)
            new_msg = True
            full_msg = b''
            break