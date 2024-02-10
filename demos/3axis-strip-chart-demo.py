
#blah blah blah


import math as m
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation as animation
from matplotlib.lines import Line2D
import time

class Strip:
    def __init__(self, ax, ay, az):
        self.ax = ax
        self.ay = ay
        self.az = az
        self.tdata = [0.0]*100
        self.xdata = [0.0]*100
        self.ydata = [0.0]*100
        self.zdata = [0.0]*100
        self.xline = Line2D(self.tdata, self.xdata)
        self.yline = Line2D(self.tdata, self.ydata)
        self.zline = Line2D(self.tdata, self.zdata)
        self.ax.add_line(self.xline)
        self.ax.set_ylim(-1.1, 1.1)
        self.ax.set_xlim(0, 10.0)
        self.ay.add_line(self.yline)
        self.ay.set_ylim(-1.1, 1.1)
        self.ay.set_xlim(0, 10.0)
        self.az.add_line(self.zline)
        self.az.set_ylim(-1.1, 1.1)
        self.az.set_xlim(0, 10.0)

    #update is called every interval to update the data and graph
    def update(self, x):
        self.tdata.append(x[0]) #append new time value
        self.tdata.pop(0)       #remove oldest time value
        self.ydata.append(x[1]) #append new ydata value
        self.xdata.pop(0)       #remove oldest ydata value
        self.xdata.append(x[1]) #append new ydata value
        self.ydata.pop(0)       #remove oldest ydata value
        self.zdata.append(x[1]) #append new ydata value
        self.zdata.pop(0)       #remove oldest ydata value
        self.xline.set_data(self.tdata, self.xdata)
        self.yline.set_data(self.tdata, self.ydata)
        self.zline.set_data(self.tdata, self.zdata)
        self.ax.set_xlim(self.tdata[0], self.tdata[0]+10.0) #shift the xlimits of the graph to match tdata range
        self.ay.set_xlim(self.tdata[0], self.tdata[0]+10.0) #shift the xlimits of the graph to match tdata range
        self.az.set_xlim(self.tdata[0], self.tdata[0]+10.0) #shift the xlimits of the graph to match tdata range
        return self.xline, self.yline, self.zline

startTime = float(time.time())
#this function is the generator, called by update, which generates the time and data values
def wave(st = startTime):
    while True:
        t = float(time.time())-startTime
        aX = m.sin(t)
        aY = m.sin(t)*m.cos(2.0*t)
        aZ = m.sin(t)*m.cos(t)
        yield t, aX, aY, aZ


fig, axes = plt.subplots(3)
scope = Strip(axes[0], axes[1], axes[2])

ani = animation.FuncAnimation(fig, scope.update, wave, interval=50, blit=True, save_count=100)

plt.show()

