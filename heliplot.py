

from matplotlib import pyplot as plt
import sys
from datetime import datetime
import scipy


ch0 = []
ch1 = []
ch2 = []
ch3 = []
cht = []

if len(sys.argv) == 1:
    print("Requires at least one argument: filenames of data file to scan.")
else:
    fileNames = sys.argv[1:]

for fileName in fileNames:
    with open(fileName,"r") as dfile:
        while True:
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
fft1 = scipy.fft.fft(ch1)
fft2 = scipy.fft.fft(ch2)
#plt.plot(fft0.real, color='black')
#plt.plot(fft0.imag, color='red')
#plt.show()
filteredfft0 = [a for a in fft0]
filteredfft1 = [a for a in fft1]
filteredfft2 = [a for a in fft2]
for i,a in enumerate(fft0):
    if i<700:#high pass
        filteredfft0[i] = 0.0
        filteredfft1[i] = 0.0
        filteredfft2[i] = 0.0
    elif i>4000:#low pass
        filteredfft0[i] = 0.0
        filteredfft1[i] = 0.0
        filteredfft2[i] = 0.0
    else:
        filteredfft0[i] = a
        filteredfft1[i] = fft1[i]
        filteredfft2[i] = fft2[i]
filtered0 = scipy.fft.ifft(filteredfft0)
filtered1 = scipy.fft.ifft(filteredfft1)
filtered2 = scipy.fft.ifft(filteredfft2)
real0 = filtered0.real
real1 = filtered1.real
real2 = filtered2.real
#plt.plot(ch0, color='black')
#plt.plot(real0, color='red')
plt.show()

#testing signal/noise discrimination in freq-space
    #it looks like good s/n in the guatematla 6.2 ch0 data is from ~700-4000
    #~700-4000 works well for ch1 also (looks generally cleaner than ch0)
    #~700-4000 works well for ch2 also (looks way cleaner than ch0 and ch1)
#noises = scipy.fft.fft(ch0[24000:34000],n=100000)
#signal = scipy.fft.fft(ch0[58000:68000],n=100000)
#noises = scipy.fft.fft(ch1[24000:34000],n=100000)
#signal = scipy.fft.fft(ch1[58000:68000],n=100000)
#noises = scipy.fft.fft(ch2[24000:34000],n=100000)
#signal = scipy.fft.fft(ch2[58000:68000],n=100000)
#plt.plot([a for a in noises.real], color='black')
#plt.plot([a for a in signal.real], color='red', alpha=0.5)
#plt.show()

heli = {}
for i in range(24):
    heli[i] = [[],[],[],[],[]]
for i,t in enumerate(cht):
    hour = int(datetime.fromtimestamp(t).strftime('%H'))
    fracHour = 60*int(datetime.fromtimestamp(t).strftime('%M'))+float(datetime.fromtimestamp(t).strftime('%S.%f'))
    heli[hour][0].append(real0[i]+5*(24-hour))
    heli[hour][1].append(real1[i]+5*(24-hour))
    heli[hour][2].append(real2[i]+5*(24-hour))
    heli[hour][4].append(fracHour)

for i in range(24):
    plt.plot(heli[i][4],heli[i][0],color='black')
plt.show()

for i in range(24):
    plt.plot(heli[i][4],heli[i][1],color='black')
plt.show()

for i in range(24):
    plt.plot(heli[i][4],heli[i][2],color='black')
plt.show()
