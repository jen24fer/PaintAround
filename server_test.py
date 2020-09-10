#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 16:53:55 2020

@author: jferina
"""

from __future__ import print_function
import sys
import socket
import numpy

try:
    import cPickle as pickle
except ImportError:
    import pickle

s = socket.socket()
s.bind((b'',8000))
s.listen(2)
while True:
    c,a = s.accept()
    data = b''
    while True:
        block = c.recv(4096)
        if not block: break
        data += block
    c.close()
    if sys.version_info.major < 3:
        unserialized_input = pickle.loads(data)
    else:
        unserialized_input = pickle.loads(data,encoding='bytes')
    print(unserialized_input)