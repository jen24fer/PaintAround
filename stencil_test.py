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


Window.clearcolor = (1, 1, 1, 1)


class StencilTestWidget(StencilView):
    '''Drag to define stencil area
    '''

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.pos = (0,0)
        self.size = (1200, 1200)
        
    # def on_touch_down(self, touch):
    #     self.pos = touch.pos
    #     self.size = (1, 1)

    # def on_touch_move(self, touch):
    #     self.size = (touch.x - touch.ox, touch.y - touch.oy)


class StencilCanvasApp(App):

    def add_rects(self, label, wid, count, *largs):
        label.text = str(int(label.text) + count)
        with wid.canvas:
            for x in range(count):
                Color(r(), 1, 1, mode='hsv')
                Rectangle(pos=(r() * wid.width + wid.x,
                               r() * wid.height + wid.y), size=(10, 10))

    def reset_stencil(self, wid, *largs):
        wid.pos = (0, 0)
        wid.size = Window.size

    def reset_rects(self, label, wid, *largs):
        label.text = '0'
        wid.canvas.clear()
        
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
        
        
        #wid.export_to_png("test.png")

    def build(self):
        wid = StencilTestWidget(size_hint=(None, None), size=Window.size)

        label = Label(text='0')

        btn_add500 = Button(text='+ 200 rects')
        btn_add500.bind(on_press=partial(self.add_rects, label, wid, 200))

        btn_reset = Button(text='Reset Rectangles')
        btn_reset.bind(on_press=partial(self.reset_rects, label, wid))

        btn_stencil = Button(text='Reset Stencil')
        btn_stencil.bind(on_press=partial(self.export, wid))

        layout = BoxLayout(size_hint=(1, None), height=50)
        layout.add_widget(btn_add500)
        layout.add_widget(btn_reset)
        layout.add_widget(btn_stencil)
        layout.add_widget(label)

        root = BoxLayout(orientation='vertical')
        rfl = FloatLayout()
        rfl.add_widget(wid)
        root.add_widget(rfl)
        root.add_widget(layout)

        return root


if __name__ == '__main__':
    StencilCanvasApp().run()
