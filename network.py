#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 10:32:00 2020

@author: Tech With Tim
"""

import socket
import pickle


class Network:
    def __init__ (self):
        print('initializing')
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "localhost"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.conne()
    
    def getP(self):
        return self.p
        
    def conne(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except Exception as e:
            print(e)
            print("Lol fail")
        
        
    def send(self, data):
        try:
            self.client.send(data)
            print("Sent: ", data)
            return pickle.loads(self.client.recv(4096*4))
        except socket.error as e:
            print(e)
            
