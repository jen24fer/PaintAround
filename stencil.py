#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import kivy
from kivy.graphics.fbo import Fbo
from kivy.graphics import Color, Rectangle, Canvas, ClearBuffers, ClearColor, Translate, Scale
from kivy.graphics.transformation import Matrix
from kivy.graphics.instructions import InstructionGroup
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

import imageio
import matplotlib.pyplot as plt
import random
import numpy as np


from kivy.config import Config
from kivy.utils import platform
import PIL
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
DRAWN_POINTS = {}
TOUCH_COUNTER = 0
STENCIL_SIZE = (0,0)

class MyBackground(Widget):
    
    texture = ObjectProperty()
    
    def __init__(self, **kwargs):
        super(MyBackground, self).__init__(**kwargs)
        with self.canvas.before:
            
            #texture = Texture.create(size=(self.size))
                    
            size = 1200 * 1200 * 3
            buf = [int(x * 255.0 / size ) for x in range(size)]
            import array
            # then, convert the array to a ubyte string
            buf = array.array('B', buf).tostring()
    
            # then blit the buffer
            #texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
            im1 = Image(source='Yosemite-Mac.jpg').texture
            #self.texture = im
            im = np.frombuffer(im1.pixels, np.uint8)
            data = np.reshape(im, (im.shape[0],1)).tostring()

            pix = np.frombuffer(data,np.uint8)
            a = np.empty_like(pix)
            texture = Texture.create(size=(1200,1200))
                    
            texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
            self.texture = texture
            self.bg = Rectangle(texture=self.texture, pos=self.pos, size=(1200,1200))

        self.bind(pos=self.update_bg)
        self.bind(size=self.update_bg)
        self.bind(texture=self.update_bg)

    def update_bg(self, *args):
        self.bg.pos = self.pos
        #self.bg.size = self.size
        self.bg.texture = self.texture

class StencilTestWidget(StencilView):
    '''Drag to define stencil area
    '''
    

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.pos = (0,0)
        #self.size = (1200, 1200)
        self.color = [1,1,1,0]
        #self.size_hint=(1.0, 1.0)
        self.size=(1200, 1200)
        self.size_hint = (1,1)
        self.id = 'stencil'
        print(self.size)
        texture = Texture.create(size=(64,64))
        # self.bg = MyBackground()
        # self.add_widget(self.bg)
        # create 64x64 rgb tab, and fill with values from 0 to 255
        # we'll have a gradient from black to white
        size = 1200 * 1200 * 3
        buf = [int(0 ) for x in range(size)]
        import array
        # then, convert the array to a ubyte string
        buf = array.array('B', buf).tostring()

        # then blit the buffer
        texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
        a = np.random.randint(low = 0, high = 255, size=(1200*1200*4,1));

        #texture = Texture.create(size=self.size)
        #texture.blit_buffer(a.tostring(), colorfmt='rgba', bufferfmt='ubyte')
        #self.image = Rectangle(pos =(0,0), size_hint = (1.0,1.0),source = 'Yosemite-Mac.jpg')
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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (1.0,1.0)
        
    def on_touch_down(self, touch):
        with self.canvas:
            Color(my_color[0],my_color[1],my_color[2],my_alpha / 100.0)
            touch.ud['line'] = Line(points=(touch.x, touch.y), width = my_linewidth)
            global DRAWN_POINTS
            global TOUCH_COUNTER
            TOUCH_COUNTER += 1
            DRAWN_POINTS[TOUCH_COUNTER] = [touch.x, touch.y]

    def on_touch_move(self, touch):
        if 'line' in touch.ud:
            touch.ud['line'].points += [touch.x, touch.y]
            global DRAWN_POINTS
            global TOUCH_COUNTER
            TOUCH_COUNTER += 1
            DRAWN_POINTS[TOUCH_COUNTER] = [touch.x, touch.y]

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
        self.size_hint = (1.0,1.0)
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

        #self.paint_widget.add_widget(self.image)
		

        self.stencil = StencilTestWidget()
        #self.image = Image(pos =(0,0), size =self.stencil.size, texture=texture)
        #self.stencil.add_widget(self.image)
        

        #self.add_widget(self.stencil)
        #self.add_widget(self.stencil)
        self.grid_layout = GridLayout(cols = 2)
        self.in_layout = GridLayout(rows = 16, size_hint=(0.25,1))
        self.bg = MyBackground()

        self.grid_layout.add_widget(self.bg)
        self.bg.add_widget(self.stencil)
        self.stencil.add_widget(self.paint_widget)
		
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
        self.clear_canvas(clearbtn)
    
    def export(self,*args):
        print("Hello there export")
        photo = Window.screenshot("test.png")
        im = imageio.imread(photo,as_gray=False)
        print(im.shape)
        plt.imshow(im)
        
    def clear_canvas(self, obj):

        self.paint_widget.canvas.clear()
        
        #self.paint_widget.canvas.ClearColor(1,1,1,0)
        clear = InstructionGroup() 
        clear.add(Color(1, 1, 1, 0)) 
        clear.add(Rectangle(pos=self.pos, size=self.size))
        self.paint_widget.canvas.add(clear)
        print(self.paint_widget.canvas.opacity)
        #self.paint_widget.canvas.draw()
            #
    
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

        
    def on_enter(self):
        num = 60        
        self.add_widget(self.count)
        def count_it(num):
            if num == 0: 
                fbo = Fbo(size=self.stencil.size, with_stencilbuffer=True)

                with fbo:
                    ClearColor(1,1, 1, 0)
                    ClearBuffers()
                    img2 = self.paintscreen.bg.texture
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
                    texture = Texture.create(size=self.stencil.size)
                    
                    texture.blit_buffer(a, colorfmt='rgba', bufferfmt='ubyte')
                    self.imge = Image(pos=(0,0), size = self.paintscreen.stencil.size, texture=texture)
                    #self.paintscreen.stencil.add_widget(self.imge)
                   
                    #img2 = self.paintscreen.grid_layout.bg.texture
                    im2 = np.frombuffer(img2.pixels, np.uint8)
                    data = np.reshape(im2, (im2.shape[0],1)).tostring()
                    

                    data2 = str(data)
                    data2 = str.encode(data2)

                    pix = np.frombuffer(data,np.uint8)
                    a2 = np.empty_like(pix)
                    a2[:] = pix
                
                    img2 = a2
                    print(img2.shape)
                    
                    print(img2)
                    img1 = a
                    print(img1.shape)

                    import cv2
                    #setting alpha=1, beta=1, gamma=0 gives direct overlay of two images
                    # in theory this would give a direct overlay...
                    #img3 = cv2.addWeighted(img1, 1, img2, 1, 0)
                    #print(img3.shape)

                    im = img1.reshape(1200,1200,4)
                    for i in range(0, 1200):
                        for j in range(0,1200):
                            points = im[i,j,:] 
                            if (points[3] == 0):#points[0] == 255 & points[1] == 255 & points[2] == 255):
                                im[i,j,:] = [255,255,255,0]
                    img_2 = img2.reshape((1200,1200,4))  
                    for i in range(0,1200):
                        for j in range(0,1200):
                            points1 =im[i,j,:]
                            if (points1[3] != 0):
                                img_2[i,j,:] = im[i,j,:]
                            
                    

                    img3 = cv2.addWeighted(img_2, 1, im, 1, 0)
                    print(img3.shape)
                    img = PIL.Image.fromarray(im ,'RGBA')            
                    img.save('img_1.png')
                    img_3 = PIL.Image.fromarray(img_2 ,'RGBA')            
                    img_3.save('img_3.png')
                    img3 = np.reshape(img3, (img3.shape[0]*img3.shape[1]*img3.shape[2],))

                    texture = Texture.create(size=(1200,1200))
                    
                    texture.blit_buffer(np.reshape(img_2,(1200*1200*4,)), colorfmt='rgba', bufferfmt='ubyte')
                    #print(img3.reshape(1200,1200,4))
                    #self.grid.bg.texture = texture
                    #self.paintscreen.stencil.add_widget(Image(texture=texture,size = self.paintscreen.stencil.size))
                
                   
                    
                    self.paintscreen = PaintScreen()
                    self.add_widget(self.paintscreen)
                    self.paintscreen.bg.texture = texture
                return
            num -= 1
            self.count.text = str(num)
            Clock.schedule_once(lambda dt: count_it(num), 1)

        Clock.schedule_once(lambda dt: count_it(1), 10)

        
        # after the clock runs out of time, we want to take a screenshot
        # photo = Window.screenshot("test.png")
        # print(photo)




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

    
    
  

class StencilCanvasApp(App):
    title = 'PaintAround'
    def build(self):
        
        self.screen_manager = ScreenManager()
        
        screen = PaintScreenContainer(name='Paint')
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




