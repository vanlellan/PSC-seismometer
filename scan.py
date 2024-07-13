
import sys
from matplotlib import pyplot as plt


ch0 = []
ch1 = []
ch2 = []
ch3 = []
cht = []

if len(sys.argv) != 2:
    print("Requires exactly one argument: filename of data file to scan.")
else:
    fileName = sys.argv[1]

with open(fileName,"r") as dfile:
    for i in range(100000):
        line = dfile.readline()
        data = line.split(',')
        ch0.append(float(data[0]))
        ch1.append(float(data[1]))
        ch2.append(float(data[2]))
        ch3.append(float(data[3]))
        cht.append(float(data[4]))

#scan through ch1, find any data points greater than 5mV from zero
trigI = []
for i,x in enumerate(ch0):
    if x>2.5 or x<-2.5:
        trigI.append(i)
#open plot of ch0,1,2 data in a window from 5s before to 25s after the trigger (~10 entries/sec)
cursor = cht[0]
for i in trigI:
    #don't open additional data points that were already within a previous plot
    if cht[i] > cursor:
        cursor = cht[i+250]
        fig, (a0, a1, a2, a3) = plt.subplots(4, sharex=True)
        a0.set_ylim(-5.0,5.0)
        a1.set_ylim(-5.0,5.0)
        a2.set_ylim(-5.0,5.0)
        a3.set_ylim(-5.0,5.0)
        a0.plot(cht[i-50:i+250],ch0[i-50:i+250])
        a1.plot(cht[i-50:i+250],ch1[i-50:i+250])
        a2.plot(cht[i-50:i+250],ch2[i-50:i+250])
        a3.plot(cht[i-50:i+250],ch3[i-50:i+250])
        a0.set_ylabel("Ch 0 (mV)")
        a1.set_ylabel("Ch 1 (mV)")
        a2.set_ylabel("Ch 2 (mV)")
        a3.set_ylabel("Ch 3 (mV)")
        a3.set_xlabel("unix time (s)")
        plt.show()

#add a sinusoidal fit to the data in each plot, output period and amplitude of the fit
