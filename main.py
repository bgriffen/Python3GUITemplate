#!/usr/bin/python
# -*- coding: utf-8 -*-
# Brendan Griffen - January 2019

from firstcalc import FirstCalc
from CommonMPL import *

class ApplicationMain(HasTraits):

    firstcalc = Instance(FirstCalc)
    display = Instance(Figure)
    markerstyle = Enum(['+',',','*','s','p','d','o'])
    markersize = Range(0,10,2)
    
    left_panel  = Group(Item('display', editor=MPLFigureEditor(),show_label=False, resizable=True),
                               HGroup(Item(name='markerstyle', label="Marker"),
                                      Item(name='markersize', label="Size")))

    right_panel = Tabbed(Item('firstcalc', style='custom', label='First Tab',show_label=False))

    view = View(HSplit(left_panel,
                 right_panel),
                width = 1280,
                height = 550,
                resizable=True,
                title="My First Python3 GUI Interface"
            )

    def _display_default(self):
        """Initialises the display."""
        figure = Figure()
        ax = figure.add_subplot(111)
        ax = figure.axes[0]
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_xlim(0,1)
        ax.set_ylim(0,1)
 
        # Set matplotlib canvas colour to be white
        rect = figure.patch
        rect.set_facecolor('w')
        return figure

    def _firstcalc_default(self):
        return FirstCalc(self)

    def _secondcalc_default(self):
        return SecondCalc(self)

    def _markercolor_changed(self):
        ax = self.display.axes[0]
        if hasattr(self, 'display_points'): 
            self.display_points.set_color(self.markercolor)
            self.display_points.set_markeredgecolor(self.markercolor)
            wx.CallAfter(self.display.canvas.draw)

    def _markerstyle_changed(self):
        ax = self.display.axes[0]
        if hasattr(self, 'display_points'): 
            self.display_points.set_marker(self.markerstyle)
            wx.CallAfter(self.display.canvas.draw)

    def _markersize_changed(self):
        ax = self.display.axes[0]
        if hasattr(self, 'display_points'): 
            self.display_points.set_markersize(self.markersize)
            wx.CallAfter(self.display.canvas.draw)

    def __init__(self, **kwargs):
        self.markercolor = 'blue'
        self.markersize = 2
        self.markerstyle = 'o'

if __name__ == '__main__':
    app = ApplicationMain()
    app.configure_traits()
