
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
for i,x in enumerate(ch1):
    if x>5.0 or x<-5.0:
        trigI.append(i)
#open plot of ch0,1,2 data in a window from 5s before to 25s after the trigger (~10 entries/sec)
cursor = cht[0]
for i in trigI:
    #don't open additional data points that were already within a previous plot
    if cht[i] > cursor:
        cursor = cht[i+250]
        fig, (ax, ay, az) = plt.subplots(3, sharex=True)
        ax.plot(cht[i-50:i+250],ch0[i-50:i+250])
        ay.plot(cht[i-50:i+250],ch1[i-50:i+250])
        az.plot(cht[i-50:i+250],ch2[i-50:i+250])
        plt.show()

#add a sinusoidal fit to the data in each plot, output period and amplitude of the fit
