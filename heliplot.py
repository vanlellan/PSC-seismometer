

from matplotlib import pyplot as plt
import sys
from datetime import datetime
import scipy


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
        if line=='':
            break
        data = line.split(',')
        ch0.append(float(data[0]))
        ch1.append(float(data[1]))
        ch2.append(float(data[2]))
        ch3.append(float(data[3]))
        cht.append(float(data[4]))

fft0 = scipy.fft.fft(ch0)
#plt.plot(fft0.real, color='black')
#plt.plot(fft0.imag, color='red')
#plt.show()
filteredfft0 = [a for a in fft0]
for i,a in enumerate(fft0):
    if i<50:#high pass
        filteredfft0[i] = 0.0
    elif i>2000:#low pass
        filteredfft0[i] = 0.0
    else:
        filteredfft0[i] = a
filtered0 = scipy.fft.ifft(filteredfft0)
real0 = filtered0.real
#plt.plot(ch0, color='black')
#plt.plot(real0, color='red')
#plt.show()

heli = {}
for i in range(24):
    heli[i] = [[],[]]
for i,t in enumerate(cht):
    hour = int(datetime.fromtimestamp(t).strftime('%H'))
    fracHour = 60*int(datetime.fromtimestamp(t).strftime('%M'))+float(datetime.fromtimestamp(t).strftime('%S.%f'))
    heli[hour][0].append(fracHour)
    heli[hour][1].append(real0[i]+5*(24-hour))

for i in range(24):
    plt.plot(heli[i][0],heli[i][1],color='black')
plt.show()
