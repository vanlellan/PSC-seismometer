#!/usr/bin/python3

#display a live-updating strip chart
#2024-02-10 Randall Evan McClellan

#This file is part of PSC-seismometer.
#
#    PSC-seismometer is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    PSC-seismometer is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with PSC-seismometer.  If not, see <http://www.gnu.org/licenses/>.


import math as m
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation as animation
from matplotlib.lines import Line2D
import time

class Strip:
    def __init__(self, ax):
        self.ax = ax
        self.tdata = [0.0]*100
        self.ydata = [0.0]*100
        self.line = Line2D(self.tdata, self.ydata)
        self.ax.add_line(self.line)
        self.ax.set_ylim(-1.1, 1.1)
        self.ax.set_xlim(0, 10.0)

    #update is called every interval to update the data and graph
    def update(self, y):
        self.tdata.append(y[0]) #append new time value
        self.tdata.pop(0)       #remove oldest time value
        self.ydata.append(y[1]) #append new ydata value
        self.ydata.pop(0)       #remove oldest ydata value
        self.line.set_data(self.tdata, self.ydata)
        self.ax.set_xlim(self.tdata[0], self.tdata[0]+10.0) #shift the xlimits of the graph to match tdata range
        return self.line,

startTime = float(time.time())
#this function is the generator, called by update, which generates the time and data values
def wave(st = startTime):
    while True:
        t = float(time.time())-startTime
        #aY = m.sin(t)
        aY = m.sin(t)*m.cos(2.0*t)
        yield t, aY


fig, ax = plt.subplots()
scope = Strip(ax)

ani = animation.FuncAnimation(fig, scope.update, wave, interval=50, blit=True, save_count=100)

plt.show()

