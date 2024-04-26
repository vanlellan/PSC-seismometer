

from matplotlib import pyplot as plt


ch0 = []
ch1 = []
ch2 = []
ch3 = []
cht = []

with open("clean22-23.txt","r") as dfile:
    for i in range(1000):
        line = dfile.readline()
        data = line.split(',')
        ch0.append(float(data[0]))
        ch1.append(float(data[1]))
        ch2.append(float(data[2]))
        ch3.append(float(data[3]))
        cht.append(float(data[4]))

ch01 = [x-y for x,y in zip(ch0,ch1)]
ch23 = [x-y for x,y in zip(ch2,ch3)]

plt.plot(ch0)
plt.show()
plt.plot(ch01)
plt.show()
plt.plot(ch23)
plt.show()
