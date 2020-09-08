#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 09:33:28 2020

@author: jferina
"""
from network import Network
import pygame
import colorsys
#from kivy.uix.slider import Slider
import kivy
kivy.require('1.8.0')
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line, Rectangle
from random import random
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.stencilview import StencilView
from kivy.uix.slider import Slider
from kivy.uix.popup import Popup
from random import random as r
from kivy.uix.gridlayout import GridLayout
from functools import partial
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.behaviors.compoundselection import CompoundSelectionBehavior
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.properties import ObjectProperty, NumericProperty, StringProperty
from kivy.clock import Clock
from kivy.uix.textinput import TextInput
from kivy.animation import Animation
from kivy.graphics import Color, Rectangle, Canvas, ClearBuffers, ClearColor
from kivy.graphics.fbo import Fbo
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.core.window import Window

from kivy.graphics.transformation import Matrix

from kivy.uix.image import Image, AsyncImage
from kivy.uix.gridlayout import GridLayout
from kivy.graphics.fbo import Fbo
from kivy.graphics.texture import Texture
from kivy.graphics.opengl import glReadPixels,GL_RGBA, GL_UNSIGNED_BYTE
from kivy.graphics import *
import pickle


import math
import random
import time
import numpy as np
import imageio
import matplotlib.pyplot as plt

# import nltk
# brown = nltk.download('brown')
# {word for word, pos in brown.tagged_words() if pos.startswith('NN')}

Window.clearcolor = (1, 1, 1, 1)

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

touch_called = False

n = Network()

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

class MyPaintWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Image(source='test0006.png'))
        
    
    def on_touch_down(self, touch):
        global touch_called
        touch_called = True
        #color = (random(), random(), random())
        with self.canvas:
            #Color(*color)
            use_alpha = my_alpha
            if (touch.x > 1200):
                print(touch.x)
                use_alpha = 0
            Color(my_color[0],my_color[1],my_color[2],use_alpha / 100.0)
            #d = 30.
            #Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
            
            touch.ud['line'] = Line(points=(touch.x, touch.y), width = my_linewidth)
            
    def on_touch_move(self, touch):
        global touch_called
        if touch_called and touch.x < 1200:
            touch.ud['line'].points += [touch.x, touch.y]
    



class IncrediblyCrudeClock5(Label):
    a = NumericProperty(5)  # seconds

    def start(self):
        Animation.cancel_all(self)  # stop any current animations
        self.anim = Animation(a=0, duration=self.a, color =[0,0,0,1])
        def finish_callback(animation, incr_crude_clock):
            incr_crude_clock.text = "FINISHED"
            # global CHANGE_TO_PAINT_SCREEN
            # if CHANGE_TO_PAINT_SCREEN:
            #     print("Changing to paint screen...")
            #     paint_app.screen_manager.current = "Paint"
            #     global SELECTED_THEME
            #     global THEMES
            #     if len(THEMES) == 0:
            #         SELECTED_THEME = ""
            #     else:
            #         SELECTED_THEME = random.sample(THEMES, 1)
            #     self.popup = Popup(title=f'Drawing: {SELECTED_THEME}',
            #                   content=Label(text="You have 30 seconds to draw!"),
            #                   size_hint=(None, None), size=(600, 400),auto_dismiss=True)
            #     self.popup.open()
            #     CHANGE_TO_PAINT_SCREEN = False
            
        self.anim.bind(on_complete=finish_callback)
        self.anim.start(self)

    def on_a(self, instance, value):
        self.text = str(round(value, 1))
        
        

class IncrediblyCrudeClock60(Label):
    a = NumericProperty(60)  # seconds

    def start(self, a):
        Animation.cancel_all(self)  # stop any current animations
        self.anim = Animation(a=0, duration=self.a, color =[0,0,0,1])
        def finish_callback(animation, incr_crude_clock):
            incr_crude_clock.text = "FINISHED"
            # global CHANGE_TO_PAINT_SCREEN
            # if CHANGE_TO_PAINT_SCREEN:
            #     print("Changing to paint screen...")
            #     paint_app.screen_manager.current = "Paint"
            #     global SELECTED_THEME
            #     global THEMES
            #     if len(THEMES) == 0:
            #         SELECTED_THEME = ""
            #     else:
            #         SELECTED_THEME = random.sample(THEMES, 1)
            #     self.popup = Popup(title=f'Drawing: {SELECTED_THEME}',
            #                   content=Label(text="You have 30 seconds to draw!"),
            #                   size_hint=(None, None), size=(600, 400),auto_dismiss=True)
            #     self.popup.open()
            #     CHANGE_TO_PAINT_SCREEN = False
            
        self.anim.bind(on_complete=finish_callback)
        self.anim.start(self)

    def on_a(self, instance, value):
        self.text = str(round(value, 1))
        #self.label = Label(text=str(round(value, 1)),color=[0,0,0,1])
# https://stackoverflow.com/questions/726549/algorithm-for-additive-color-mixing-for-rgb-values
# def blendColorValue(a, b, t):
#     return math.sqrt((1 - t) * a^2 + t * b^2)

# def blendAlphaValue(a, b, t):
#     return (1-t)*a + t*b;

    
    # ret
    
    
    # [r, g, b].each n ->
    #     ret[n] = blendColorValue(c1[n], c2[n], t)
    # ret.alpha = blendAlphaValue(c1.alpha, c2.alpha, t)
    # return ret


# class ScreenManagement(ScreenManager):
#     pass


# class Progress(Popup):

#     def __init__(self, **kwargs):
#         super(Progress, self).__init__(**kwargs)
#         # call dismiss_popup in 2 seconds
#         Clock.schedule_once(self.dismiss_popup, 90)

#     def dismiss_popup(self, dt):
#         self.dismiss()

class MainMenu(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.message = Label(halign="center",valign="middle",font_size=30,color=[0,0,0,1])
        self.message.bind(width=self.update_text_width)
        self.add_widget(self.message)
        menubtn = Button(text = "Start Game")
        menubtn.bind(on_release = self.play_game)
        self.add_widget(menubtn)
        
    def update_info(self, message):
        self.message.text = message

    def update_text_width(self, *_):
        self.message.text_size = (self.message.width*0.9, None)
        
    def play_game(self,obj):
        paint_app.screen_manager.current = "EnterTopics"


class PaintScreen(GridLayout):
    
  
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        left = True
        switch = False
        space_h = 10
        start_h = 1300
        space_v = 10
        start_v = 45
        size_paint = 100
        iters = 0
        # self.cols = 2
        # self.rows = 2
        #wid = StencilTestWidget(size_hint=(None, None), size=(1300,1300))
        # self.parent = Widget()
        
        self.painter = MyPaintWidget()

        clearbtn = Button(text='Clear', pos=(1350,1100))
        clearbtn.bind(on_release=self.clear_canvas)
        
        
        mixbtn = Button(text='Mix', pos = (1350, 850))
        mixbtn.bind(on_release=self.mix_colors)
        
        switchbtn = Button(text="Switch", pos = (1450,1100))
        switchbtn.bind(on_release=self.switch_button)
        
        changeAlpha = Slider(min=0,max=100, pos =(1350,1000), sensitivity = 'handle')
        changeAlpha.bind(value=self.change_alpha)
        
        changeLinewidth = Slider(min=0,max=100,pos=(1350,930), sensitivity = 'handle')
        changeLinewidth.bind(value=self.change_linewidth)
        self.add_widget(Label(text='Brush Width', pos=(1350,970), color=(0,0,0,1)))
        self.add_widget(changeLinewidth)
        self.add_widget(changeAlpha)       
        self.add_widget(Label(text='Water (Transparency)', pos=(1350,1040), color=(0,0,0,1)))
        

        #parent.add_widget(self.painter)
        self.add_widget(self.painter)
        
        #parent.add_widget(wid)
        #self.crudeclock = IncrediblyCrudeClock()
        
        #self.add_widget(self.crudeclock)
        #self.crudeclock.start()
        
            #return grid
        
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
            self.add_widget(col_button)
    
        self.add_widget(clearbtn)
        self.add_widget(mixbtn)
        self.add_widget(switchbtn)
        

        # boxLayout = BoxLayout(orientation = 'horizontal')
        # label = Label(text='List as many \n themes as you can \n think of'
        #               ' in \n 90 seconds!')
        # boxLayout.add_widget(label)
        # popup = Popup(title='Create Themes',
        #               content=boxLayout,
        #               size_hint=(None, None), size=(1000, 1000),auto_dismiss=True)
       
        #parent.add_widget(popup)
        
        #return parent
    
    # def on_enter(self):
    #     print("ENtereing screen")
    #     global SELECTED_THEME
    #     global THEMES
    #     if len(THEMES) == 0:
    #         SELECTED_THEME = ""
    #     else:
    #         SELECTED_THEME = random.sample(THEMES, 1)
    #     self.popup = Popup(title=f'Drawing: {SELECTED_THEME}',
    #                   content=Label(text="You have 30 seconds to draw!"),
    #                   size_hint=(None, None), size=(600, 400),auto_dismiss=True)
    #     self.popup.open()
    
    def export(self,*args):
        print("Hello there export")
        photo = Window.screenshot("test.png")
        im = imageio.imread(photo,as_gray=False)
        print(im.shape)
        plt.imshow(im)

        im2 = im[0:1199, 0:1199, :]
        #im2 = np.array(im2, np.uint8)
        # send the image to the server
        global n
        n.send(pickle.dumps("im2"))
        #n.send(pickle.dumps(im2))
        
        #self.painter.export_to_png("test.png")
        # # if self.parent is not None:
        # #     canvas_parent_index = self.parent.canvas.indexof(self.canvas)
        # #     self.parent.canvas.remove(self.canvas)
        # fbo = Fbo(size=self.size, with_stencilbuffer=True)

        # with fbo:
        #     ClearColor(1, 1, 1, 1)
        #     ClearBuffers()
        #     #Scale(1, -1, 1)
        #     #Translate(-self.x, -self.y - self.height, 0)
        #     #self.painter.export_to_png("test2.png")
            
        #     Scale(1, -1, 1)
        #     Translate(-self.painter.x, -self.painter.y - self.painter.height, 0)
        #     Window.screenshot("test.png")
        #     fbo.add(self.painter.canvas)
        #     #fbo.draw()
        #     fbo.texture.save("gidhup.png", flipped=False)
        #     #fbo.remove(self.painter.canvas)
        
    def clear_canvas(self, obj):
        self.painter.canvas.clear()
    
    def change_color(self, obj):
        global my_color 
        my_color = obj.background_color
        
    def change_alpha(self, obj, alpha):
        global touch_called
        global my_alpha
        my_alpha = alpha
        touch_called = False
    
    def change_linewidth(self, obj, linewidth):
        global my_linewidth
        my_linewidth = linewidth
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
        exitbtn = Button(text = "Done",
                         size_hint=(0.215, 0.075))
        mixbutt = Button(text = 'Mix',size_hint=(0.215, 0.075),pos = (50,50))
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
        boxLayout.add_widget(mixbutt)
        boxLayout.add_widget(grid)
        popup = Popup(title='Mix Colors',
                      content=boxLayout,
                      size_hint=(None, None), size=(600, 400),auto_dismiss=False)
       
        exitbtn.bind(on_press = popup.dismiss)
        # backgroundcolors = []
        # for ch in grid.children:
        #     backgroundcolors.append(ch.background_color) 
        mixbutt.bind(on_press = self.mix)
        popup.open()

    def switch_button(self, obj):
        info = "Switching screen"
        paint_app.main_menu.update_info(info)
        paint_app.screen_manager.current = "Main"
  

class ImageTest(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        im = Image(source="test0006.png")
        self.add_widget(im)
        

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
        self.switchbtn.bind(on_release = self.switch_button)
        self.add_widget(self.switchbtn)
        
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
        
            
    def switch_button(self, obj):
        info = "Switching screen"
        paint_app.main_menu.update_info(info)
        #paint_app.screen_manager.current = "Paint"
        #clock = IncrediblyCrudeClock();
        #paint_app.screen_manager.current.add_widget(clock)
        #paint_app.screen_manager.current.clock.start()
        paint_app.screen_manager.switch_to(paint_app.screens[3])



class PaintScreenContainer(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.paintscreen = PaintScreen()
        self.add_widget(self.paintscreen)
        self.count = Label(text="", pos=(720, 300),font_size=45,color=[0,0,0,1])
        
        
    def on_enter(self):
        print("Entered the screen")
        # self.crudeclock = IncrediblyCrudeClock5()
        # self.add_widget(self.crudeclock)
        # self.crudeclock.start()
        num = 60
        
        self.add_widget(self.count)
        def count_it(num):
            if num == 0: 
                self.paintscreen.export()
                return
            num -= 1
            self.count.text = str(num)
            Clock.schedule_once(lambda dt: count_it(num), 1)

        Clock.schedule_once(lambda dt: count_it(5), 0)
        # after the clock runs out of time, we want to take a screenshot
        # photo = Window.screenshot("test.png")
        # print(photo)
        
        #self.paintscreen.export()

            
class MyPaintApp(App):
    
    def build(self):
        self.screen_manager = ScreenManager()

        self.screens = []
        self.main_menu = MainMenu()
        screen = Screen(name = 'Main')
        screen.add_widget(self.main_menu)
        self.screen_manager.add_widget(screen)
        self.screens.append(screen)
        
        self.enter_topics = EnterTopics()
        screen = Screen(name = 'EnterTopics')
        screen.add_widget(self.enter_topics)
        self.screen_manager.add_widget(screen)
        self.screens.append(screen)
        
        
        self.paint_screen = PaintScreen()
        screen = Screen(name = 'Paint')
        screen.add_widget(self.paint_screen)
        self.screen_manager.add_widget(screen)
        
        self.screens.append(screen)
        
        screen = PaintScreenContainer()
        self.screens.append(screen)
        
    
        return self.screen_manager
        # my_screenmanager = ScreenManager()
        # screen1 = PaintScreen(name='paintscreen')
        # screen2 = MainMenu(name='mainmenu')
        # my_screenmanager.add_widget(screen1)
        # my_screenmanager.add_widget(screen2)
        # return my_screenmanager
        
            
        # parent.add_widget(grid)
if __name__ == '__main__':
    paint_app = MyPaintApp()
    paint_app.run()
    





# pygame.init()
# width = 700
# height = 600
# BLACK = pygame.Color( 0 ,  0 ,  0 )
# WHITE = pygame.Color(255, 255, 255)
# BLUE = pygame.Color(200,200,255)

# WINSORYELLOW = pygame.Color(255,229,15)
# WINSORYELLOWDEEP = pygame.Color(255, 200, 53)
# CADMIUMRED = pygame.Color(227,0,34)
# ALIZARINCRIMSON = pygame.Color(227,38,54)
# PERMANENTROSE = pygame.Color(237,54,110)
# FRENCHULTRAMARINE = pygame.Color(9,77,158)
# WINSORBLUEGREENSHADE = pygame.Color(15,97,137)
# CERULEANBLUE = pygame.Color(2,136,197)
# WINSORGREENBLUESHADE = pygame.Color(6,153,125)
# WINSORGREENYELLOWSHADE = pygame.Color(115,193,117)
# YELLOWOCHRE = pygame.Color(244,167,79)
# BURNTSIENNA = pygame.Color(173,83,74)

# PAINT_COLORS = [WINSORYELLOW, WINSORYELLOWDEEP, CADMIUMRED, ALIZARINCRIMSON,
#                 PERMANENTROSE, FRENCHULTRAMARINE, WINSORBLUEGREENSHADE,
#                 CERULEANBLUE, WINSORGREENBLUESHADE, WINSORGREENYELLOWSHADE, 
#                 YELLOWOCHRE, BURNTSIENNA]


# win = pygame.display.set_mode((width, height))
# canvas = win.copy()

# canvas.fill(pygame.color.THECOLORS['antiquewhite2'])
# pygame.display.set_caption("Client")
# clock = pygame.time.Clock()

# pygame.time.set_timer(pygame.USEREVENT, 1000)
# font = pygame.font.SysFont('Consolas', 30)

# colors = list(pygame.color.THECOLORS.values())
# cols = [[x[0],x[1],x[2]] for x in colors]



# class Button:
#     def __init__(self,text,x,y,color):
#         self.text = text
#         self.x = x
#         self.y = y
#         self.color = color
#         self.width = 150
#         self.height = 100
    
#     def draw(self, win):
#         pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
#         font = pygame.font.SysFont("papyrus", 40)
#         text = font.render(self.text, 1, (255,255,255))
#         # center the text
#         win.blit(text, (self.x + round(self.width / 2 ) - round(text.get_width() / 2), self.y + round(self.width / 2 ) - round(text.get_width() / 2)))
        

#     def click(self, pos):
#         x1 = pos[0]
#         y1 = pos[1]
#         return self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height
           
#     def color(self):
#         return self.color
# def redrawWindow(win,game, p):
#     win.fill((255,255,255))
    
#     # left_pressed, middle_pressed, right_pressed = pygame.mouse.get_pressed()
#     # if left_pressed:
#     #     pygame.draw.circle(canvas, BLACK, (pygame.mouse.get_pos()),5)
#     win.blit(canvas, (0, 0))
#     if not(game.connected()):
#         font = pygame.font.SysFont("papyrus", 80)
# #        text = font.render("Waiting for Player...", 1, (255,0,0), True)
# #        win.blit(text, (width/2 - text.get_width (), height /2 - text. get_height()))
#     else:
#         font = pygame.font.SysFont("papyrus", 60)
# #        text = font.render("Your Move", 1, (0,255,0), True)
# #        win.blit(text, (80,200))
        
# #        text = font.render("Opponent's Move", 1, (0,255,0), True)
# #        win.blit(text, (380,200))
        
# #         move1 = game.get_player_move(0)
# #         move2 = game.get_player_move(1)
        
# #         if game.bothWent():
# #             text1 = font.render(move1, 1, (0,0,0))
# #             text2 = font.render(move2, 1, (0,0,0))
# #         else:
# # #            if game.p1Went and p == 0:
# #                text1 = font.render(move1, 1, (0,0,0))
# #            elif game.p1Went:
# #                text1 = font.render("Locked In", 1, (0,0,0))
# #            else:
# #                text1 = font.render("Waiting", 1, (0,0,0))
            
# #            if game.p2Went and p == 1:
# #                text2 = font.render(move2, 1, (0,0,0))
# #            elif game.p2Went:
# #                text2 = font.render("Locked In", 1, (0,0,0))
# #            else:
# #                text2 = font.render("Waiting", 1, (0,0,0))
 
                
#         # if p ==1:
#         #     win.blit(text2, (100, 350))
#         #     win.blit(text1, (400, 350))
#         # else:
#         #     win.blit(text1, (100, 350))
#         #     win.blit(text2, (400, 350))
                
# #        for btn in btns:
# #            btn.draw(win)
            
#     pygame.display.update()
# #btns = [Button("Rock", 50,500,(0,0,0)), Button("Scissors", 250,500, (255,0,0)), Button("Paper", 450,500,(0,255,0))]
# pos = pygame.mouse.get_pos()
# btns = []
# left = True
# switch = False
# space_h = 10
# start_h = 500
# space_v = 10
# start_v = 45
# size_paint = 75
# iters = 0

# for color in PAINT_COLORS:
#     if iters % 2 == 0 and iters != 0:
#         switch = True
#     else:
#         switch = False
#     if switch:
#         start_v += (size_paint + space_v)
#     if left:
#         btn = Button("", start_h+space_h,start_v,color)
#         #pygame.draw.rect(canvas,color,(start_h+space_h,start_v,size_paint,size_paint))
#     if not left:
#         btn = Button("", start_h+space_h*2+size_paint,start_v,color)#pygame.draw.rect(canvas,color,(start_h+space_h*2+size_paint,start_v,size_paint,size_paint))
#     left = not left
#     btn.draw(canvas)
#     btns.append(btn)
#     iters += 1
# pygame.display.update()  


# s = Slider(min=-100, max=100, value=25)


# def main():
#     COLORVAR = BLACK
#     pos = (0,0)
#     run = True
#     clock = pygame.time.Clock()
#     n = Network()
#     player = int(n.getP())
#     print("You are player ", player)
#     drawing = False
#     last_pos = None
#     #pygame.draw.rect(canvas,BLUE,(500,0,200,700))
      
#     while run:
#         #clock.tick(60)
#         try:
#             game = n.send("get")
#         except Exception as e:
#             print(e)
#             run = False
#             print("Couldn't get game, failed at sending get 1")
#             break
#         # if game.bothWent():
#         #     redrawWindow(win, game, player)
#         #     pygame.time.delay(200)
#         #     try:
#         #         game = n.send("reset")
#         #     except Exception as e:
#         #         print(e)
#         #         run = False
#         #         print("Couldn't get game, failed at sending reset 2")
#         #         break
#         #     font = pygame.font.SysFont("papyrus", 90)
#         #     if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
#         #         #text = font.render("You Won!",1,(255,0,0))
#         #         pass
#         #     elif game.winner() == -1:
#         #         #text = font.render("Tie Game!", 1, (255,0,0))
#         #         pass
#         #     else:
#         #         #text = font.render("You Lost...", 1, (255,0,0))
#         #         pass
                
# #            win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))    
#             # pygame.display.update()
#             # pygame.time.delay(2000)
#         counter, text = 10, '10'.rjust(3)

#         for event in pygame.event.get():
#             counter -= 1
#             text = str(counter).rjust(3) if counter > 0 else 'boom!'
#             if event.type == pygame.QUIT:
#                 run = False
#                 pygame.quit()
#             # if event.type == pygame.MOUSEBUTTONDOWN:
#             #     pos = pygame.mouse.get_pos()
#             #     pygame.draw.circle(win, BLACK, (pygame.mouse.get_pos()), 5)
#             elif event.type == pygame.MOUSEMOTION:
#                 if (drawing):
#                     mouse_position = pygame.mouse.get_pos()
#                     if last_pos is not None:
#                         pygame.draw.line(canvas, COLORVAR, last_pos, mouse_position, 1)
#                     last_pos = mouse_position
#             elif event.type == pygame.MOUSEBUTTONUP:
#                  mouse_position = (0, 0)
#                  drawing = False
#                  last_pos = None
#             elif event.type == pygame.MOUSEBUTTONDOWN:
#                  drawing = True
#                  print("Drawing now...")
#                  pos = pygame.mouse.get_pos()
#                  print(pos)
#             # text = font.render(text, 1, (0, 0, 0))
#             # win.blit(text, (100,300))
#             # pygame.display.flip()
#             # clock.tick(60)
#             # continue
            
#             for btn in btns:
#                 if btn.click(pos):
#                     print("clicked")
#                     COLORVAR = btn.color;
#                     # change the color of the mouse
                    
#                     # if player == 0:
#                     #     if not game.p1Went:
#                     #         n.send(btn.text) # the text of the button is the move
#                     # else:
#                     #     if not game.p2Went:
#                     #         n.send(btn.text) 
#                 # for btn in btns:
#                 #     if btn.click(pos) and game.connected():
#                 #         if player == 0:
#                 #             if not game.p1Went:
#                 #                 n.send(btn.text) # the text of the button is the move
#                 #         else:
#                 #             if not game.p2Went:
#                 #                 n.send(btn.text) 
#         redrawWindow(win, game, player)
#         pygame.display.update()
    
# def menu_screen():
#     run = True

#     while run:
#         win.fill((255,255,255))
        
#         clock.tick(60)
#         font = pygame.font.SysFont("papyrus", 60)
#         text = font.render("Click to Play!", 1, (255,0,0))
#         win.blit(text, (100,200))
#         pygame.display.update()
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 run = False
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 run = False
                
    
#     main()
    
# while True:
#     menu_screen()