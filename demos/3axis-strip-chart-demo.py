#!/usr/bin/python3

#strip chart demo for 3-dimensional seismometer data
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
    def __init__(self, ax, ay, az, resolution=10, tmax=5):
        self.ax = ax
        self.ay = ay
        self.az = az
        self.resolution = resolution
        self.tmax = tmax
        self.tdata = [0.0]*(tmax*1000//(resolution+10)) #there's an extra ~10ms delay of processing time at each iteration, I think
        self.xdata = [0.0]*(tmax*1000//(resolution+10))
        self.ydata = [0.0]*(tmax*1000//(resolution+10))
        self.zdata = [0.0]*(tmax*1000//(resolution+10))
        self.xline = Line2D(self.tdata, self.xdata)
        self.yline = Line2D(self.tdata, self.ydata)
        self.zline = Line2D(self.tdata, self.zdata)
        self.ax.add_line(self.xline)
        self.ax.set_ylim(-1.1, 1.1)
        self.ax.set_xlim(0, self.tmax+1)
        self.ay.add_line(self.yline)
        self.ay.set_ylim(-1.1, 1.1)
        self.ay.set_xlim(0, self.tmax+1)
        self.az.add_line(self.zline)
        self.az.set_ylim(-1.1, 1.1)
        self.az.set_xlim(0, self.tmax+1)

    #update is called every interval to update the data and graph
    def update(self, x):
        self.tdata.append(x[0]) #append new time value
        self.tdata.pop(0)       #remove oldest time value
        self.ydata.append(x[1]) #append new xdata value
        self.xdata.pop(0)       #remove oldest xdata value
        self.xdata.append(x[2]) #append new ydata value
        self.ydata.pop(0)       #remove oldest ydata value
        self.zdata.append(x[3]) #append new zdata value
        self.zdata.pop(0)       #remove oldest zdata value
        self.xline.set_data(self.tdata, self.xdata)
        self.yline.set_data(self.tdata, self.ydata)
        self.zline.set_data(self.tdata, self.zdata)
        self.ax.set_xlim(self.tdata[0], self.tdata[0]+self.tmax+1) #shift the xlimits of the xgraph to match tdata range + 1s extra
        self.ay.set_xlim(self.tdata[0], self.tdata[0]+self.tmax+1) #shift the xlimits of the ygraph to match tdata range + 1s extra
        self.az.set_xlim(self.tdata[0], self.tdata[0]+self.tmax+1) #shift the xlimits of the zgraph to match tdata range + 1s extra
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


fig, (ax, ay, az) = plt.subplots(3,sharex=True)
scope = Strip(ax, ay, az)

ani = animation.FuncAnimation(fig, scope.update, wave, interval=scope.resolution, blit=True, save_count=5)

plt.show()

