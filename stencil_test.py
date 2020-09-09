#!/usr/bin/env python3
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
from kivy.graphics.fbo import Fbo
from kivy.graphics import Color, Rectangle, Canvas, ClearBuffers, ClearColor, Translate, Scale
from kivy.graphics.transformation import Matrix
#from kivy.uix.image import Image, AsyncImage
from kivy.app import App
from kivy.core.window import Window
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

from kivy.uix.image import Image, AsyncImage
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition

from kivy.uix.slider import Slider

import imageio
import matplotlib.pyplot as plt
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



class StencilTestWidget(StencilView):
    '''Drag to define stencil area
    '''
    

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.pos = (0,0)
        self.size = (1200, 1200)
        self.color = [0,0,0,1]
        
    # def on_touch_down(self, touch):
    #     self.pos = touch.pos
    #     self.size = (1, 1)

    # def on_touch_move(self, touch):
    #     self.size = (touch.x - touch.ox, touch.y - touch.oy)



    def export(self, wid, *largs):
        # if self.parent is not None:
        #     canvas_parent_index = self.parent.canvas.indexof(self.canvas)
        #     self.parent.canvas.remove(self.canvas)

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








class StencilCanvasApp(App):
        
    def build(self):
        #wid = StencilTestWidget(size_hint=(None, None), size=Window.size)

        #label = Label(text='0')

        #btn_add500 = Button(text='+ 200 rects')
        #btn_add500.bind(on_press=partial(self.add_rects, label, wid, 200))

        #btn_reset = Button(text='Reset Rectangles')
        #btn_reset.bind(on_press=partial(self.reset_rects, label, wid))

        # btn_stencil = Button(text='Take Screenshot')
        # btn_stencil.bind(on_press=partial(self.export, wid))

        # layout = BoxLayout(size_hint=(1, None), height=50)
        # #layout.add_widget(btn_add500)
        # #layout.add_widget(btn_reset)
        # layout.add_widget(btn_stencil)
        # #layout.add_widget(label)

        # root = BoxLayout(orientation='vertical')
        # rfl2 = BoxLayout(orientation='vertical')
        # rfl = FloatLayout()
        # wid.add_widget(MyPaintWidget())
        # rfl.add_widget(wid)
        # #rfl.add_widget(btn_stencil)
        # root.add_widget(rfl)
        # root.add_widget(layout)
        
        self.screen_manager = ScreenManager()

        self.screens = []
        # self.main_menu = MainMenu()
        # screen = Screen(name = 'Main')
        # screen.add_widget(self.main_menu)
        # self.screen_manager.add_widget(screen)
        # self.screens.append(screen)
        
        # self.enter_topics = EnterTopics()
        # screen = Screen(name = 'EnterTopics')
        # screen.add_widget(self.enter_topics)
        # self.screen_manager.add_widget(screen)
        # self.screens.append(screen)
        
        
        # self.paint_screen = PaintScreen()
        # screen = Screen(name = 'Paint')
        # screen.add_widget(self.paint_screen)
        # self.screen_manager.add_widget(screen)
        
        # self.screens.append(screen)
        
        screen = PaintScreenContainer()
        self.screens.append(screen)
        self.screen_manager.add_widget(screen)
    
        return self.screen_manager

        # return root
    


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

#         # self.cols = 2
#         # self.rows = 2
#         wid = StencilTestWidget(size_hint=(None, None), size=(1300,1300))
#         # self.parent = Widget()
        
#         self.painter = MyPaintWidget()
        self.paint_widget = MyPaintWidget()
        self.stencil = StencilTestWidget(size_hint=(None, None), size=(1200,1200),id = 'stencil')
        self.stencil.add_widget(self.paint_widget)
        self.add_widget(self.stencil)
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


#         #parent.add_widget(self.painter)
#         self.add_widget(self.painter)
        
#         #parent.add_widget(wid)
#         #self.crudeclock = IncrediblyCrudeClock()
        
#         #self.add_widget(self.crudeclock)
#         #self.crudeclock.start()
        
#             #return grid
        
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
        

#         # boxLayout = BoxLayout(orientation = 'horizontal')
#         # label = Label(text='List as many \n themes as you can \n think of'
#         #               ' in \n 90 seconds!')
#         # boxLayout.add_widget(label)
#         # popup = Popup(title='Create Themes',
#         #               content=boxLayout,
#         #               size_hint=(None, None), size=(1000, 1000),auto_dismiss=True)
       
#         #parent.add_widget(popup)
        
#         #return parent
    
#     # def on_enter(self):
#     #     print("ENtereing screen")
#     #     global SELECTED_THEME
#     #     global THEMES
#     #     if len(THEMES) == 0:
#     #         SELECTED_THEME = ""
#     #     else:
#     #         SELECTED_THEME = random.sample(THEMES, 1)
#     #     self.popup = Popup(title=f'Drawing: {SELECTED_THEME}',
#     #                   content=Label(text="You have 30 seconds to draw!"),
#     #                   size_hint=(None, None), size=(600, 400),auto_dismiss=True)
#     #     self.popup.open()
    
    def export(self,*args):
        print("Hello there export")
        photo = Window.screenshot("test.png")
        im = imageio.imread(photo,as_gray=False)
        print(im.shape)
        plt.imshow(im)

#         im2 = im[0:1199, 0:1199, :]
#         #im2 = np.array(im2, np.uint8)
#         # send the image to the server
#         global n
#         n.send(pickle.dumps("im2"))
#         #n.send(pickle.dumps(im2))
        
#         #self.painter.export_to_png("test.png")
#         # # if self.parent is not None:
#         # #     canvas_parent_index = self.parent.canvas.indexof(self.canvas)
#         # #     self.parent.canvas.remove(self.canvas)
#         # fbo = Fbo(size=self.size, with_stencilbuffer=True)

#         # with fbo:
#         #     ClearColor(1, 1, 1, 1)
#         #     ClearBuffers()
#         #     #Scale(1, -1, 1)
#         #     #Translate(-self.x, -self.y - self.height, 0)
#         #     #self.painter.export_to_png("test2.png")
            
#         #     Scale(1, -1, 1)
#         #     Translate(-self.painter.x, -self.painter.y - self.painter.height, 0)
#         #     Window.screenshot("test.png")
#         #     fbo.add(self.painter.canvas)
#         #     #fbo.draw()
#         #     fbo.texture.save("gidhup.png", flipped=False)
#         #     #fbo.remove(self.painter.canvas)
        
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
        # paint_app.main_menu.update_info(info)
        # paint_app.screen_manager.current = "Main"
  

# class ImageTest(Image):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         im = Image(source="test0006.png")
#         self.add_widget(im)


class PaintScreenContainer(Screen):
    
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.paintscreen = PaintScreen()
        self.add_widget(self.paintscreen)
        self.count = Label(text="", pos=(720, 300),font_size=45,color=[0,0,0,1])
        for child in self.paintscreen.children[:]:
            if child.id == 'stencil':
                self.stencil = child
    
        
    def on_enter(self):
        print("Entered the screen")
        # self.crudeclock = IncrediblyCrudeClock5()
        # self.add_widget(self.crudeclock)
        # self.crudeclock.start()
        num = 60
        
        self.add_widget(self.count)
        def count_it(num):
            if num == 0: 
                fbo = Fbo(size=self.stencil.size, with_stencilbuffer=True)

                with fbo:
                    ClearColor(1,1, 1, 1)
                    ClearBuffers()
                    #Scale(1, -1, 1)
                    #Translate(-self.x, -self.y - self.height, 0)
                
                    fbo.add(self.stencil.canvas)
                    fbo.draw()
                    img = fbo.texture
                    img.save('test.png')
                    fbo.remove(self.stencil.canvas)
                    self.remove_widget(self.paintscreen)
                    self.paintscreen = PaintScreen()
                    self.add_widget(self.paintscreen)
                        #self.paintscreen.export()
                        
                        #self.paintexport(self.stencil)
                return
            num -= 1
            self.count.text = str(num)
            Clock.schedule_once(lambda dt: count_it(num), 1)

        Clock.schedule_once(lambda dt: count_it(5), 0)
        # after the clock runs out of time, we want to take a screenshot
        # photo = Window.screenshot("test.png")
        # print(photo)
        
        #self.paintscreen.export()


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




if __name__ == '__main__':
    StencilCanvasApp().run()


