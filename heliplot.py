
import matplotlib
matplotlib.use('GTK3Agg')
import matplotlib.pyplot as plt

import sys
import os
#from datetime import datetime, date, UTC, timedelta, timezone
from datetime import datetime, date, timedelta, timezone
from scipy.fftpack import fft, ifft

def updateTime():
    targetDay = datetime.now(timezone.utc) - timedelta(days=0)
    targetStamp = int(targetDay.timestamp())
    #targetMin = datetime.fromtimestamp(targetStamp, UTC).replace(hour=0, minute=0, second=0, microsecond=0)
    #targetMax = datetime.fromtimestamp(targetStamp, UTC).replace(hour=23, minute=59, second=59, microsecond=999999)
    targetMin = datetime.utcfromtimestamp(targetStamp).replace(hour=0, minute=0, second=0, microsecond=0)
    targetMax = datetime.utcfromtimestamp(targetStamp).replace(hour=23, minute=59, second=59, microsecond=999999)
    targetMinStamp = targetMin.timestamp()
    targetMaxStamp = targetMax.timestamp()
    print("targetStampDiff: ", targetMaxStamp-targetMinStamp)
    return (targetDay, targetMinStamp, targetMaxStamp)

if len(sys.argv) != 2:
    print("Requires exactly one argument: path to directory of data files.")
    sys.exit(0)
else:
    fileDir = sys.argv[1]

def getData(dataDir, dataTime):
    fileNames = [dataDir+f for f in os.listdir(dataDir) if os.path.isfile(os.path.join(dataDir, f))]
    #print("fileNames: ", fileNames)

    dataRaw = {}
    dataFFT = {}
    for i in range(24):
        dataRaw[i] = [[],[],[],[],[]]
        dataFFT[i] = [[],[],[],[],[]]
    
    for fileName in fileNames:
        #only open files that could contain data from today i.e. date(filename) == target or target+1, files are ~2.67 hours long
        fileInt = int(fileName[-14:-4])
        timezoneFudge = 3600*5
        if fileInt>=int(dataTime[1]-3600*3-timezoneFudge) and fileInt<=int(dataTime[2]):
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
                    if float(tFloat)>dataTime[1]-timezoneFudge and float(tFloat)<dataTime[2]:
                        dataRaw[tHour][0].append(float(data[0]))
                        dataRaw[tHour][1].append(float(data[1]))
                        dataRaw[tHour][2].append(float(data[2]))
                        #dataRaw[tHour][3].append(float(data[3]))
                        dataRaw[tHour][4].append(tFloat)
                        #fracHour = 60*int(datetime.fromtimestamp(tFloat,UTC).strftime('%M'))+float(datetime.fromtimestamp(tFloat,UTC).strftime('%S.%f'))
                        fracHour = 60*int(datetime.utcfromtimestamp(tFloat).strftime('%M'))+float(datetime.utcfromtimestamp(tFloat).strftime('%S.%f'))
                        dataFFT[tHour][4].append(fracHour)
    
    for ii in range(24):
        N = len(dataRaw[ii][4])
    #    print("N = ", N)
        for jj in range(3):
            if len(dataRaw[ii][jj]) == 0:
                continue
            rawfft = fft(dataRaw[ii][jj])
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
            dataFFT[ii][jj] = real
    #        if ii==2 and jj==0:
    #            plt.plot(fft.real, color='black')
    #            plt.plot(fft.imag, color='red')
    #            plt.show()
    #            plt.plot(dataRaw[ii][jj], color='black')
    #            plt.plot(dataFFT[ii][jj], color='red')
    #            plt.show()
    return dataFFT
    
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

while True:

    targetTime = updateTime()
    heliFFT = getData(fileDir, targetTime)
   
    f, ax = plt.subplots(3,1,sharex=True)
    f.tight_layout()
    f.subplots_adjust(hspace=0)

    for i in heliFFT:
        templine, = ax[0].plot([t/60 for t in heliFFT[i][4]], [(a/5)+i for a in heliFFT[i][1]],color='black',linestyle='solid')
        #if i==0:
        #    templine.set_label("Ch 1")
    
    for i in heliFFT:
        templine, = ax[1].plot([t/60 for t in heliFFT[i][4]] ,[(a/5)+i for a in heliFFT[i][2]],color='purple',linestyle='solid')
        #if i==0:
        #    templine.set_label("Ch 0")
    
    for i in heliFFT:
        templine, = ax[2].plot([t/60 for t in heliFFT[i][4]] ,[(a/5)+i for a in heliFFT[i][0]],color='green',linestyle='solid')
        #if i==0:
        #    templine.set_label("Ch 2")
    plt.xlabel("time (minutes)", fontsize=20)
    ar = [a.twinx() for a in ax]
    DIR = ["Vertical", "East-West", "North-South"]
    for j in range(3):
        #ax[j].legend(loc='upper right',fontsize=20)
        ax[j].set_ylim([-0.9,23.9])
        ax[j].set_xlim([-5,65])
        ax[j].yaxis.set_major_locator(plt.MultipleLocator(1))
        #iticklabels = [item.get_text()+":00" for item in ax[j].get_yticklabels()]
        #ax[j].set_yticklabels(ticklabels)
        ax[j].invert_yaxis()
        ax[j].set_ylabel("time (hours UTC)", fontsize=15)
        ar[j].set_ylabel(DIR[j], fontsize=25)
        ar[j].tick_params(right=False, labelright=False)
    f.suptitle(targetTime[0].strftime('PSC Seismometer, %b %d, %Y'), fontsize=30, y=0.98)
    f.canvas.manager.window.move(2500,100)
    plt.get_current_fig_manager().full_screen_toggle()
    plt.show(block=False)
    plt.pause(600.0)   #pause for ten minutes between plot updates
    plt.close()
