#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 18:53:53 2020

@author: Tech With Tim
"""

class Player():
    def __init__(self, name):
        self.name = name
        print("Name has been created ", self.name)
        # self.y = y
        # self.width = width
        # self.height = height
        # self.color = color
        # self.rect = (x,y,width,height)
        # self.vel = 3
    

    # def draw(self, win):
    #     pygame.draw.rect(win, self.color, self.rect)
    
    # def move(self):
        
        # keys = pygame.key.get_pressed()
        
        # if keys[pygame.K_LEFT]:
        #     self.x -= self.vel
        # if keys[pygame.K_RIGHT]:
        #     self.x += self.vel
        # if keys[pygame.K_UP]:
        #     self.y -= self.vel
        # if keys[pygame.K_DOWN]:
        #     self.y += self.vel
        # self.update()
    
    # def get_image(self):
        
        
    def update(self): 
        self.rect = (self.x, self.y, self.width, self.height)