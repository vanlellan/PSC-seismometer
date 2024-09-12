

from matplotlib import pyplot as plt
import sys
import os
#from datetime import datetime, date, UTC, timedelta, timezone
from datetime import datetime, date, timedelta, timezone
from scipy.fftpack import fft, ifft

targetDay = datetime.now(timezone.utc) - timedelta(days=20)
targetStamp = int(targetDay.timestamp())
#targetMin = datetime.fromtimestamp(targetStamp, UTC).replace(hour=0, minute=0, second=0, microsecond=0)
#targetMax = datetime.fromtimestamp(targetStamp, UTC).replace(hour=23, minute=59, second=59, microsecond=999999)
targetMin = datetime.utcfromtimestamp(targetStamp).replace(hour=0, minute=0, second=0, microsecond=0)
targetMax = datetime.utcfromtimestamp(targetStamp).replace(hour=23, minute=59, second=59, microsecond=999999)
targetMinStamp = targetMin.timestamp()
targetMaxStamp = targetMax.timestamp()

ch0 = []
ch1 = []
ch2 = []
ch3 = []
cht = []

if len(sys.argv) != 2:
    print("Requires exactly one argument: path to directory of data files.")
else:
    fileDir = sys.argv[1]
    fileNames = [fileDir+f for f in os.listdir(fileDir) if os.path.isfile(os.path.join(fileDir, f))]
    print("fileNames: ", fileNames)

heliRaw = {}
heliFFT = {}
for i in range(24):
    heliRaw[i] = [[],[],[],[],[]]
    heliFFT[i] = [[],[],[],[],[]]

for fileName in fileNames:
    #only open files that could contain data from today i.e. date(filename) == target or target+1, files are ~2.67 hours long
    fileInt = int(fileName[-14:-4])
    if fileInt>=int(targetMinStamp-3600*3) and fileInt<=int(targetMaxStamp):
        print("Reading in: ", fileName)
        with open(fileName,"r") as dfile:
            while True:
                line = dfile.readline()
                if line=='':
                    break
                data = line.split(',')
                tFloat = float(data[4])
                #tHour = int(datetime.fromtimestamp(tFloat,UTC).strftime('%H'))
                tHour = int(datetime.utcfromtimestamp(tFloat).strftime('%H'))
                #only load data from target day, group by hour within each channel
                if float(tFloat)>targetMinStamp and float(tFloat)<targetMaxStamp:
                    heliRaw[tHour][0].append(float(data[0]))
                    heliRaw[tHour][1].append(float(data[1]))
                    heliRaw[tHour][2].append(float(data[2]))
                    #heliRaw[tHour][3].append(float(data[3]))
                    heliRaw[tHour][4].append(tFloat)
                    #fracHour = 60*int(datetime.fromtimestamp(tFloat,UTC).strftime('%M'))+float(datetime.fromtimestamp(tFloat,UTC).strftime('%S.%f'))
                    fracHour = 60*int(datetime.utcfromtimestamp(tFloat).strftime('%M'))+float(datetime.utcfromtimestamp(tFloat).strftime('%S.%f'))
                    heliFFT[tHour][4].append(fracHour)

for ii in range(24):
    N = len(heliRaw[ii][4])
#    print("N = ", N)
    for jj in range(3):
        if len(heliRaw[ii][jj]) == 0:
            continue
        rawfft = fft(heliRaw[ii][jj])
        filteredfft = [a for a in rawfft]
        for i,a in enumerate(rawfft):
            if i<(N//150):#high pass, i=250 for N=37500 (one hour), approx 0.0667 Hz
                filteredfft[i] = 0.0
            elif i>(N//25):#low pass, i=1500 for N=37500 (one hour), approx 0.4 Hz
                filteredfft[i] = 0.0
            else:
                filteredfft[i] = a
        filtered = ifft(filteredfft)
        real = filtered.real
        heliFFT[ii][jj] = real
#        if ii==2 and jj==0:
#            plt.plot(fft.real, color='black')
#            plt.plot(fft.imag, color='red')
#            plt.show()
#            plt.plot(heliRaw[ii][jj], color='black')
#            plt.plot(heliFFT[ii][jj], color='red')
#            plt.show()

#testing signal/noise discrimination in freq-space
    #it looks like good s/n in the guatematla 6.2 ch0 data is from ~700-4000
    #~700-4000 works well for ch1 also (looks generally cleaner than ch0)
    #~700-4000 works well for ch2 also (looks way cleaner than ch0 and ch1)
#noises = scipy.fft.fft(heliRaw[2][2][250:1250])
#signal = scipy.fft.fft(heliRaw[3][2][250:1250])
#noises = scipy.fft.fft(ch1[24000:34000],n=100000)
#signal = scipy.fft.fft(ch1[58000:68000],n=100000)
#noises = scipy.fft.fft(ch2[24000:34000],n=100000)
#signal = scipy.fft.fft(ch2[58000:68000],n=100000)
#plt.plot([a for a in noises.real], color='black')
#plt.plot([a for a in signal.real], color='red', alpha=0.5)
#plt.show()

for i in heliFFT:
    templine, = plt.plot([t/60 for t in heliFFT[i][4]], [(a/5)+i for a in heliFFT[i][1]],color='black',linestyle='solid')
    if i==0:
        templine.set_label("Ch 1")
#plt.show(block=False)
#plt.pause(5.0)
#plt.close()

for i in heliFFT:
    templine, = plt.plot([t/60 for t in heliFFT[i][4]] ,[(a/5)+i for a in heliFFT[i][0]],color='purple',linestyle='dashed')
    if i==0:
        templine.set_label("Ch 0")
#plt.show(block=False)
#plt.pause(5.0)
#plt.close()

for i in heliFFT:
    templine, = plt.plot([t/60 for t in heliFFT[i][4]] ,[(a/5)+i for a in heliFFT[i][2]],color='green',linestyle='dotted')
    if i==0:
        templine.set_label("Ch 2")
plt.xlabel("time (minutes)")
plt.ylabel("time (hours UTC)")
plt.legend()
plt.gca().set_ylim([-0.9,23.9])
plt.gca().set_xlim([-5,65])
plt.gca().yaxis.set_major_locator(plt.MultipleLocator(1))
ticklabels = [item.get_text()+":00" for item in plt.gca().get_yticklabels()]
plt.gca().set_yticklabels(ticklabels)
plt.gca().invert_yaxis()
plt.title(targetDay.strftime('PSC Seismometer, %b %d, %Y'))
plt.get_current_fig_manager().full_screen_toggle()
plt.show()
