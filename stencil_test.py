#!/usr/bin/env python3 -u
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 09:12:21 2020

@author: kivy repo authors
https://github.com/kivy/kivy/blob/master/examples/canvas/stencil_canvas.py
"""

  
'''
Stencil demo
============
This is a test of the stencil graphics instruction inside the stencil view
widget. When you use a stencil, nothing will be drawn outside the bounding
box. All the graphics will draw only in the stencil view.
You can "draw" a stencil view by touch & draw. The touch down will set the
position, and the drag will set the size.
'''
import kivy
from kivy.graphics.fbo import Fbo
from kivy.graphics import Color, Rectangle, Canvas, ClearBuffers, ClearColor, Translate, Scale
from kivy.graphics.transformation import Matrix
#from kivy.uix.image import Image, AsyncImage
from kivy.app import App

from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.stencilview import StencilView
from random import random as r
from functools import partial
from kivy.factory import Factory
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line
from kivy.uix.gridlayout import GridLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.behaviors.compoundselection import CompoundSelectionBehavior
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty, NumericProperty, StringProperty
from kivy.graphics.texture import Texture

from kivy.uix.image import Image, AsyncImage
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition

from kivy.uix.slider import Slider
from kivy.uix.textinput import TextInput
from network import Network

import imageio
import matplotlib.pyplot as plt
import random
import pickle
import io
import numpy as np
from game import Game
from player import Player
import struct
import os
import sys
import socket_client
from kivy.config import Config
from kivy.utils import platform

Config.set('graphics', 'resizable', 0)
from kivy.core.window import Window
Window.clearcolor = (1, 1, 1, 1)
print(Window.system_size)
print(Window.size)
#Window.size = (kivy.metrics.dp(600), kivy.metrics.dp(400))
WINSORYELLOW = (255/255.0,229/255.0,15/255.0)
WINSORYELLOWDEEP = (255/255.0, 200/255.0, 53/255.0)
CADMIUMRED = (227/255.0,0/255.0,34/255.0)
ALIZARINCRIMSON = (227/255.0,38/255.0,54/255.0)
PERMANENTROSE = (237/255.0,54/255.0,110/255.0)
FRENCHULTRAMARINE = (9/255.0,77/255.0,158/255.0)
WINSORBLUEGREENSHADE = (15/255.0,97/255.0,137/255.0)
CERULEANBLUE = (2/255.0,136/255.0,197/255.0)
WINSORGREENBLUESHADE = (6/255.0,153/255.0,125/255.0)
WINSORGREENYELLOWSHADE = (115/255.0,193/255.0,117/255.0)
YELLOWOCHRE = (244/255.0,167/255.0,79/255.0)
BURNTSIENNA = (173/255.0,83/255.0,74/255.0)
WHITE = (1,1,1)
BLACK = (0,0,0)
PAINT_COLORS = [WINSORYELLOW, WINSORYELLOWDEEP, CADMIUMRED, ALIZARINCRIMSON,
                PERMANENTROSE, FRENCHULTRAMARINE, WINSORBLUEGREENSHADE,
                CERULEANBLUE, WINSORGREENBLUESHADE, WINSORGREENYELLOWSHADE, 
                YELLOWOCHRE, BURNTSIENNA, BLACK, WHITE]
PAINT_COLORS = PAINT_COLORS[::-1] 
BACKGROUND_NODES = []
THEMES = set()
SELECTED_THEME = []
CHANGE_TO_PAINT_SCREEN = False
my_color = [0, 0, 0]
my_alpha = 100.0
my_linewidth = 1.0



class StencilTestWidget(StencilView):
    '''Drag to define stencil area
    '''
    

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.pos = (0,0)
        #self.size = (1200, 1200)
        self.color = [0,0,0,1]
        #self.size_hint=(1.0, 1.0)
        self.size=(1200, 1200)
        self.id = 'stencil'
        print(self.size)
        texture = Texture.create(size=(64,64))
        # create 64x64 rgb tab, and fill with values from 0 to 255
        # we'll have a gradient from black to white
        size = 1200 * 1200 * 3
        buf = [int(x * 255 / size) for x in range(size)]
        import array
        # then, convert the array to a ubyte string
        buf = array.array('B', buf).tostring()

        # then blit the buffer
        texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
        a = np.random.randint(low = 0, high = 255, size=(1200*1200*4,1));
        #texture = Texture.create(size=self.size)
        #texture.blit_buffer(a.tostring(), colorfmt='rgba', bufferfmt='ubyte')
        self.image = Image(pos =(0,0), size_hint =(1.0,1.0), texture=texture)
        #self.add_widget(self.image)

    def export(self, wid, *largs):

        fbo = Fbo(size=wid.size, with_stencilbuffer=True)

        with fbo:
            ClearColor(1,1, 1, 1)
            ClearBuffers()
            #Scale(1, -1, 1)
            #Translate(-self.x, -self.y - self.height, 0)
        
        fbo.add(wid.canvas)
        fbo.draw()
        img = fbo.texture
        img.save('test.png')
        fbo.remove(wid.canvas)










class MyPaintWidget(Widget):

    def on_touch_down(self, touch):
        with self.canvas:
            Color(my_color[0],my_color[1],my_color[2],my_alpha / 100.0)
            touch.ud['line'] = Line(points=(touch.x, touch.y), width = my_linewidth)

    def on_touch_move(self, touch):
        if 'line' in touch.ud:
            touch.ud['line'].points += [touch.x, touch.y]

class PaintScreen(GridLayout):
  
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.add_widget()
        left = True
        switch = False
        space_h = 10
        start_h = 1300
        space_v = 10
        start_v = 45
        size_paint = 100
        iters = 0
        #self.grid_layout = GridLayout(cols = 2, rows = 1)
        self.rows = 1
        self.cols = 2
        self.paint_widget = MyPaintWidget()
        texture = Texture.create(size=(64,64))
        # create 64x64 rgb tab, and fill with values from 0 to 255
        # we'll have a gradient from black to white
        size = 1200 * 1200 * 3
        buf = [int(x * 255 / size) for x in range(size)]
        import array
        # then, convert the array to a ubyte string
        buf = array.array('B', buf).tostring()

        # then blit the buffer
        texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
        a = np.random.randint(low = 0, high = 255, size=(1200*1200*4,1));
        #texture = Texture.create(size=self.size)
        #texture.blit_buffer(a.tostring(), colorfmt='rgba', bufferfmt='ubyte')
        self.image = Image(pos =(0,0), size =(1200,1200), texture=texture)
        #self.paint_widget.add_widget(self.image)
		
		
        self.stencil = StencilTestWidget()
        self.stencil.add_widget(self.image)
        self.stencil.add_widget(self.paint_widget)
		
        #self.add_widget(self.stencil)
        self.grid_layout = GridLayout(cols = 2)
        self.in_layout = GridLayout(rows = 16, size_hint=(0.25,1))
        self.grid_layout.add_widget(self.stencil)
		
        clearbtn = Button(text='Clear', pos=(1350,1100))
        clearbtn.bind(on_release=self.clear_canvas)
        self.in_layout.add_widget(clearbtn)
        
        #self.add_widget(self.grid_layout)
        mixbtn = Button(text='Mix', pos = (1350, 850))
        mixbtn.bind(on_release=self.mix_colors)
        
        switchbtn = Button(text="Switch", pos = (1450,1100))
        switchbtn.bind(on_release=self.switch_button)
        
        changeAlpha = Slider(min=0,max=100, pos =(1350,1000), sensitivity = 'handle')
        changeAlpha.bind(value=self.change_alpha)
        self.in_layout.add_widget(mixbtn)
        self.in_layout.add_widget(switchbtn)
        self.in_layout.add_widget(Label(text=""))
        
        self.in_layout.add_widget(Label(text="Transparency", color=(0,0,0,1)))
        self.in_layout.add_widget(changeAlpha)
        
        changeLinewidth = Slider(min=0,max=100,pos=(1350,930), sensitivity = 'handle')
        changeLinewidth.bind(value=self.change_linewidth)
        # self.add_widget(Label(text='Brush Width', pos=(1350,970), color=(0,0,0,1)))
        # self.add_widget(changeLinewidth)
        # self.add_widget(changeAlpha)       
        # self.add_widget(Label(text='Water (Transparency)', pos=(1350,1040), color=(0,0,0,1)))
        self.in_layout.add_widget(Label(text="Brush Width", color=(0,0,0,1)))
        self.in_layout.add_widget(changeLinewidth)
        
        for col in PAINT_COLORS:
            if iters % 2 == 0 and iters != 0:
                switch = True
            else:
                switch = False
            if switch:
                start_v += (size_paint + space_v)
            if left:
                col_button = Button(text='',  
                    background_color =(col[0], col[1], col[2], 1),
                    pos =(start_h+space_h,start_v))
            if not left:
                col_button = Button(text='',  
                    background_color =(col[0], col[1], col[2], 1),
                    pos =(start_h+space_h*2+size_paint,start_v ))
            left = not left
            iters += 1

            col_button.bind(on_release=self.change_color)
            self.in_layout.add_widget(col_button)
        self.grid_layout.add_widget(self.in_layout)
        self.add_widget(self.grid_layout)
		
		
        # self.add_widget(clearbtn)
        # self.add_widget(mixbtn)
        # self.add_widget(switchbtn)
    

    
    def export(self,*args):
        print("Hello there export")
        photo = Window.screenshot("test.png")
        im = imageio.imread(photo,as_gray=False)
        print(im.shape)
        plt.imshow(im)
        
    def clear_canvas(self, obj):
        self.paint_widget.canvas.clear()
    
    def change_color(self, obj):
        global my_color 
        my_color = obj.background_color
        
    def change_alpha(self, obj, alpha):
        print("changing alpha")
        global touch_called
        global my_alpha
        my_alpha = alpha
        # touch_called = False
    
    def change_linewidth(self, obj, linewidth):
        print("changing linewidth")
        global my_linewidth
        my_linewidth = linewidth
        print(my_linewidth)
        global touch_called
        touch_called = False
        
    def mix(self,obj):
        finalColor = [0,0,0,0]
        print(f"obj is {obj}")
        global BACKGROUND_NODES
        colorList = BACKGROUND_NODES
        #print(f"The length of the colors is: {len(colorList)}")
        for c in colorList:
            finalColor[0] += c[0]
            finalColor[1] += c[1]
            finalColor[2] += c[2]
            finalColor[3] += c[3]
            
            finalColor[0] /= len(colorList)
            finalColor[1] /= len(colorList)
            finalColor[2] /= len(colorList)
            finalColor[3] /= len(colorList)
        
        global my_color
        my_color = finalColor
        #return finalColor
        print(my_color)
        
    def mix_colors(self,obj):
        label = Label(text='Select any amount \n of colors to mix\n from the palette')
        exitbtn = Button(text = "Done")
        mixbutt = Button(text = 'Mix',pos = (50,50))
        random_button = Button(text = "Random", pos=(100,100))
        grid = SelectableGrid(cols=2, rows=7, touch_multiselect=True,
                              multiselect=True)
        for i in range(0,len(PAINT_COLORS)):
            col = PAINT_COLORS[i]
            col_button = Button(text='',  
                    background_color =(col[0], col[1], col[2], 1))
            col_button.bind(on_release=self.change_color)
            grid.add_widget(col_button)
        
        
        
        boxLayout = BoxLayout(orientation = 'horizontal')
        boxLayout.add_widget(label)
        boxLayout.add_widget(exitbtn)
        boxLayout.add_widget(random_button)
        boxLayout.add_widget(mixbutt)
        
        boxLayout.add_widget(grid)
        
        popup = Popup(title='Mix Colors',
                      content=boxLayout,
                      size_hint=(0.8,0.6),auto_dismiss=False, pos_hint={'x': 0.1, 
                            'y':0})
       
        exitbtn.bind(on_press = popup.dismiss)
        # backgroundcolors = []
        # for ch in grid.children:
        #     backgroundcolors.append(ch.background_color) 
        mixbutt.bind(on_press = self.mix)
        random_button.bind(on_release = self.random_color)
        popup.open()

    def switch_button(self, obj):
        info = "Switching screen"
        # paint_app.main_menu.update_info(info)
        # paint_app.screen_manager.current = "Main"
  
    def random_color(self, obj):
        global my_color 
        color = [random.randint(0,255)/255.0 for i in range(0,3)]
        my_color = color#(random.randint(0,255), random.randint(0,255), random.randint(0,255))
        print(my_color)


class PaintScreenContainer(Screen):
    
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.paintscreen = PaintScreen()
        self.add_widget(self.paintscreen)
        self.count = Label(text="", pos=(720, 300),font_size=45,color=[0,0,0,1])
        self.grid = self.paintscreen
        self.stencil = self.grid.stencil
        # for child in self.grid.children[:]:
                # if child.id == 'stencil':
                    # self.stencil = child

        
    def on_enter(self):
        print("Entered the screen")
        
        global SELECTED_THEME
        global THEMES
        if len(THEMES) == 0:
            SELECTED_THEME = ""
        else:
            SELECTED_THEME = random.sample(THEMES, 1)
        self.popup = Popup(title=f'Drawing: {str(SELECTED_THEME)}',
                      content=Label(text="You have 30 seconds to draw!"),
                      size_hint=(None, None), size=(600, 400),auto_dismiss=True)
        self.popup.open()
        #self.popup.close()
        #Clock.schedule_once(self.close_popup, 3)
        paint_app.title = SELECTED_THEME
        

        num = 60
          
        self.add_widget(self.count)
        def count_it(num):
            if num == 0: 
                fbo = Fbo(size=self.stencil.size, with_stencilbuffer=True)

                with fbo:
                    ClearColor(1,1, 1, 1)
                    ClearBuffers()
                
                    fbo.add(self.stencil.canvas)
                    fbo.draw()
                    img = fbo.texture
                    fbo.remove(self.stencil.canvas)
                    self.remove_widget(self.paintscreen)
                    im = np.frombuffer(img.pixels, np.uint8)
                    data = np.reshape(im, (im.shape[0],1)).tostring()
                    

                    data2 = str(data)
                    data2 = str.encode(data2)

                    pix = np.frombuffer(data,np.uint8)
                    a = np.empty_like(pix)
                    a[:] = pix
                    print(a)
                    print("Shape of a is ", a.shape)
                    print("Type of a is ", type(a))
                    texture = Texture.create(size=self.stencil.size)
                    
                    texture.blit_buffer(a, colorfmt='rgba', bufferfmt='ubyte')
                    print("Sending...")
                    
                    # import socket
                    # import pickle
                    # import matplotlib.pyplot as plt
                    
                    # HEADERSIZE = 10
                    
                    # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    # s.connect((socket.gethostname(), 1235))
                    # msglen = HEADERSIZE
                   
                    # full_msg = b''
                    # new_msg = True
                    # while True:
                    #     msg = s.recv(msglen)
                    #     if new_msg:
                    #         print("new msg len:",msg[:HEADERSIZE])
                    #         msglen = int(msg[:HEADERSIZE])
                    #         new_msg = False
                
                    #     print(f"full message length: {msglen}")
                
                    #     full_msg += msg
                
                    #     print(len(full_msg))
                
                
                    #     if len(full_msg)-HEADERSIZE == msglen:
                    #         print("full msg recvd")
                    #         d = pickle.loads(full_msg[HEADERSIZE:])
                    #         #plt.imshow(d)
                    #         print(d.shape)
                    #         new_msg = True
                    #         full_msg = b''
                    #         break
                    
                   
                    # d = np.reshape(d, (5760000))
                    # print("Shape of d is ", d.shape)
                    # print("Type of d is ", type(d))

                    # buf = [int(x * 255 / (1200*1200*4)) for x in range(1200*1200*4)]
                    # import array
                    # d = d.tolist()
                   
                    # d = array.array('B',d).tostring()
                    # texture.blit_buffer(d , colorfmt='rgba', bufferfmt='ubyte')

                    socket_client.send(a)
                    
 
                    self.imge = Image( pos =(0,0), size = (1200,1200), texture=texture)
                    #self.add_widget(self.imge)
                    self.paintscreen = PaintScreen()
                    self.paintscreen.stencil.image = self.imge
                    self.add_widget(self.paintscreen)
                    #socket_client.send(pickle.dumps(np.ones((1200*1200,1))))
                return
            num -= 1
            self.count.text = str(num)
            Clock.schedule_once(lambda dt: count_it(num), 1)

        Clock.schedule_once(lambda dt: count_it(1), 10)

        
        # after the clock runs out of time, we want to take a screenshot
        # photo = Window.screenshot("test.png")
        # print(photo)
        
        #self.paintscreen.export()

    # def close_popup(self):
    #     self.popup.dismiss()



class SelectableGrid(FocusBehavior, CompoundSelectionBehavior, GridLayout):

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        """Based on FocusBehavior that provides automatic keyboard
        access, key presses will be used to select children.
        """
        if super(SelectableGrid, self).keyboard_on_key_down(
            window, keycode, text, modifiers):
            return True
        if self.select_with_key_down(window, keycode, text, modifiers):
            return True
        return False

    def keyboard_on_key_up(self, window, keycode):
        """Based on FocusBehavior that provides automatic keyboard
        access, key release will be used to select children.
        """
        if super(SelectableGrid, self).keyboard_on_key_up(window, keycode):
            return True
        if self.select_with_key_up(window, keycode):
            return True
        return False

    def add_widget(self, widget):
        """ Override the adding of widgets so we can bind and catch their
        *on_touch_down* events. """
        widget.bind(on_touch_down=self.button_touch_down,
                    on_touch_up=self.button_touch_up)
        return super(SelectableGrid, self).add_widget(widget)

    def button_touch_down(self, button, touch):
        """ Use collision detection to select buttons when the touch occurs
        within their area. """
        if button.collide_point(*touch.pos):
            self.select_with_touch(button, touch)

    def button_touch_up(self, button, touch):
        """ Use collision detection to de-select buttons when the touch
        occurs outside their area and *touch_multiselect* is not True. """
        if not (button.collide_point(*touch.pos) or
                self.touch_multiselect):
            self.deselect_node(button)

    def select_node(self, node):
        #node.border = (10,10,10,10)
        node.background_color = (node.background_color[0], 
                                 node.background_color[1], 
                                 node.background_color[2], 0.1)
        return super(SelectableGrid, self).select_node(node)

    def deselect_node(self, node):
        node.background_color = (node.background_color[0], 
                                 node.background_color[1], 
                                 node.background_color[2], 1)
        super(SelectableGrid, self).deselect_node(node)

    def on_selected_nodes(self, gird, nodes):
        print("Selected nodes = {0}".format(nodes))
        global BACKGROUND_NODES
        BACKGROUND_NODES = []
        for node in nodes:
            BACKGROUND_NODES.append(node.background_color)
        print(f"Background nodes is {BACKGROUND_NODES}")





class EnterTopics(GridLayout):
    

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.rows = 3
        global THEMES
        THEMES = set()
        # self.message = Label(halign="center",valign="middle",font_size=30,color=[0,0,0,1])
        # self.message.bind(width=self.update_text_width)
        # self.add_widget(self.message)
        self.switchbtn = Button(text="Switch")
        #self.switchbtn.bind(on_release = self.switch_button)
        #self.add_widget(self.switchbtn)
        
        self.history = Label(text = 'Submit Themes to Paint (submit after each theme).  You have 30 seconds!',
                             height = Window.size[1]*0.4, size_hint_y=None,color=[0,0,0,1])
        self.add_widget(self.history)
        #self.crudeclock = IncrediblyCrudeClock()
        
        #self.add_widget(self.crudeclock)
        
        
        self.topic = TextInput(text="", multiline=False)
        
        
        self.send = Button(text = "Submit")
        self.send.bind(on_release=self.send_text)
        
        bottom_line = GridLayout(cols=3)
        bottom_line.add_widget(self.topic)
        bottom_line.add_widget(self.send)

        self.add_widget(bottom_line)


    def send_text(self, obj):
        global THEMES
        if self.topic.text != "":
            THEMES.add(self.topic.text)
        print(THEMES)
        self.topic.text = ""

    def text_changed(self, obj):
        print("Animation complete!")
        paint_app.screen_manager.current = "Paint"
        
            
    # def switch_button(self, obj):
    #     info = "Switching screen"
    #     #paint_app.main_menu.update_info(info)
    #     #paint_app.screen_manager.current = "Paint"
    #     #clock = IncrediblyCrudeClock();
    #     #paint_app.screen_manager.current.add_widget(clock)
    #     #paint_app.screen_manager.current.clock.start()
    #     paint_app.screen_manager.switch_to(paint_app.screens[2])
        
class EnterTopicsScreenContainer(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.count = Label(text="Test", pos=(720, 300),font_size=45,color=[0,0,0,1])
        self.enter_topics = EnterTopics()
        self.add_widget(self.enter_topics)
    
    def on_enter(self):
        print("Entering the topic screen")
        num = 30
        self.add_widget(self.count)
        def count_it(num):
            if num == 0: 
                
                return
            num -= 1
            print(num)
            self.count.text = str(num)
            self.count.text = str(num)
            Clock.schedule_once(lambda dt: count_it(num), 1)

        Clock.schedule_once(lambda dt: count_it(5), 0)
        print("executed stuff here?") 
        Clock.schedule_once(self.switch, 5)
        
    def switch(self,obj):
        print("switching...s")
        self.remove_widget(self.count)
        paint_app.screen_manager.switch_to(paint_app.screens[3])

class MainMenu(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 2
        self.rows = 4
        
        if (os.path.isfile("prev_details.txt")):
            with open("prev_details.txt", "r") as f:
                d = f.read().split(",")
                prev_ip = d[0]
                prev_port = d[1]
                prev_username = d[2]
                print("it is a file")
        else:
            prev_ip = ""
            prev_port = ""
            prev_username = ""
        
        self.add_widget(Label(text="IP:",color=[0,0,0,1]))
        self.ip = TextInput(text=prev_ip,multiline = False)
        self.add_widget(self.ip)
        
        self.add_widget(Label(text="Port:",color=[0,0,0,1]))
        self.port = TextInput(text=prev_port,multiline = False)
        self.add_widget(self.port)
        
        
        self.add_widget(Label(text="Username:",color=[0,0,0,1]))
        self.username = TextInput(text=prev_username,multiline = False)
        self.add_widget(self.username)
        #self.message = Label(halign="center",valign="middle",font_size=30,color=[0,0,0,1])
        #self.message.bind(width=self.update_text_width)
       # self.add_widget(self.message)
        self.add_widget(Label())
        menubtn = Button(text = "Start Game")
        menubtn.bind(on_release = self.play_game)
        self.add_widget(menubtn)
        
    def update_info(self, message):
        self.message.text = message

    def update_text_width(self, *_):
        self.message.text_size = (self.message.width*0.9, None)
        
    def play_game(self,obj):
        port = self.port.text
        ip = self.ip.text
        username = self.username.text
        
        
        
        with open("prev_details.txt", "w") as f:
            f.write(f"{ip},{port},{username}")
        
        info = f"Attempting to join {ip}:{port} as {username}"
        paint_app.loading_screen.update_info(info)
        paint_app.screen_manager.switch_to(paint_app.screens[1])
        
        Clock.schedule_once(self.connect,1)
    
    def connect(self,_):
        port = int(self.port.text)
        ip = self.ip.text
        username = self.username.text
        p = Player(username)
        g = Game(1)
        if not socket_client.connect(ip, port, username, show_error):
            return
        paint_app.screen_manager.switch_to(paint_app.screens[2])
    
    
    
    
def show_error(message):
    paint_app.loading_screen.update_info(message)

    paint_app.screen_manager.current = 'LoadingScreen'
    Clock.schedule_once(sys.exit, 10)
        
class LoadingScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols= 1
        self.message = Label(halign='center', valign='middle', font_size =30, color=[0,0,0,1])
        self.message.bind(width = self.update_text_width)
        self.add_widget(self.message)
        
    def update_info(self, message):
        self.message.text = message
        
    def update_text_width(self, *_):
        self.message.text_size = (self.message.width*0.9, None)
    
    
    
    def on_enter(self):
        pass
        # game = Game(100)
        # # p2pos = n.send(str.encode("Ready"))
        # # player2.x = p2pos
        
        # if not(game.connected()):
        #     label = Label(text="Waiting for players to connect...", color=[0,0,0,1])
        #     paint_app.screen_manager.switch_to(paint_app.screens[2])
        # else:
        #     label = Label(text="Players connected",color = [0,0,0,1])
        #     paint_app.screen_manager.switch_to(paint_app.screens[2])
        # self.add_widget(label)
    
class JoiningScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols= 1
        self.message = Label(halign='center', valign='middle', font_size =30, color=[1,0,0,1], text="Waiting for players to join...")
        self.message.bind(width = self.update_text_width)
        self.add_widget(self.message)
        
    # def update_info(self, message):
    #     self.message.text = message
        
    def update_text_width(self, *_):
        self.message.text_size = (self.message.width*0.9, None)
    
    
    
    def on_enter(self):
        self.message.text = "Waiting for players to join..."
        try:
            no = socket_client.startGame("Go")
            self.message.text = str(no)
        except Exception as e:
            print(e)
            print("Couldn't get game")

class StencilCanvasApp(App):
    title = 'PaintAround'
    def build(self):
        
        self.screen_manager = ScreenManager()

        self.screens = []
        self.main_menu = MainMenu()
        screen = Screen(name = 'Main')
        screen.add_widget(self.main_menu)
        self.screen_manager.add_widget(screen)
        self.screens.append(screen)
        
        screen = LoadingScreen(name="Load")
        self.loading_screen = screen
        self.screen_manager.add_widget(screen)
        self.screens.append(screen)
        
        # screen = JoiningScreen(name ="Join")
        # self.joining_screen = screen
        # self.screen_manager.add_widget(screen)
        # self.screens.append(screen)
        # screen = EnterTopicsScreenContainer()
        # self.screen_manager.add_widget(screen)
        # self.screens.append(screen)
        
        screen = PaintScreenContainer(name='Paint')
        self.screens.append(screen)
        self.screen_manager.add_widget(screen)
    
        return self.screen_manager

        # return root
   
def read_pos(s):
    #s = s.split(",")
    return np.fromstring(s, sep = ',')


def make_pos(arr):
    return np.array2string(arr)

if __name__ == '__main__':
    #n = Network() 
    if platform == 'macosx':
        print("Mac!")
    paint_app = StencilCanvasApp()
    #player = int(n.getP())
    #print("You are player ", player)
    # while True:
    #     game = n.send(str.encode("reset"))
    #     if game.connected():
    #         print("Game connected!")
    #         break

    paint_app.run()




