#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 20:33:19 2020

@author: Tech with Tim
"""
class Game:
    def __init__(self, iden):
        # self.p1Went = False
        # self.p2Went = False
        # self.ready = False
        # self.id = iden
        # self.moves = [None, None]
        # self.wins = [0,0]
        # self.ties = 0
        print("Creating a new game with id ", iden)
        
    def get_player_move(self, p):
        """

        Parameters
        ----------
        p : p: [0,1]
            DESCRIPTION.

        Returns
        -------
        Move.

        """
        return self.moves[p]

    def play(self, player, move):
        self.moves[player] = move
        if player == 0:
            self.p1Went = True
        else:
            self.p2Went = True
    
    def connected(self):
        return self.ready
    
    def bothWent(self):
        return self.p1Went and self.p2Went
    
    def winner(self):
        p1 = self.moves[0].upper()[0]
        p2 = self.moves[1].upper()[0]
        
        winner = -1
        if p1 == 'R' and p2 == 'S':
            winner = 0
        elif p1 == 'S' and p2 == 'R':
            winner = 1
        elif p1 == 'P' and p2 == 'R':
            winner = 0
        elif p1 == 'R' and p2 == 'P':
            winner = 1
        elif p1 == 'S' and p2 == 'P':
            winner = 0
        elif p1 == 'P' and p2 == 'S':
            winner = 1
        
        return winner
            
    def resetWent(self):
        self.p1Went = False
        self.p2Went = False
        