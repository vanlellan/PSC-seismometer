

from matplotlib import pyplot as plt


ch0 = []
ch1 = []
ch2 = []
ch3 = []
cht = []

#with open("seismodiff.txt","r") as dfile:
with open("panama51.txt","r") as dfile:
    for i in range(1000):
        line = dfile.readline()
        if True:
            data = line.split(',')
            ch0.append(float(data[0]))
            ch1.append(float(data[1]))
            ch2.append(float(data[2]))
            ch3.append(float(data[3]))
            cht.append(float(data[4]))


plt.plot(ch0)
plt.show()
plt.plot(ch1)
plt.show()
plt.plot(ch2)
plt.show()
plt.plot(ch3)
plt.show()
