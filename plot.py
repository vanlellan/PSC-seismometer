

from matplotlib import pyplot as plt


ch0 = []
ch1 = []
ch2 = []
ch3 = []
cht = []

with open("seismo.txt","r") as dfile:
    for i in range(500):
        line = dfile.readline()
        if True:
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
plt.plot(ch1)
plt.show()
plt.plot(ch01)
plt.show()
plt.plot(ch23)
plt.show()
