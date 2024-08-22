

from matplotlib import pyplot as plt
import sys


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

#ch01 = [x-y for x,y in zip(ch0,ch1)]
#ch23 = [x-y for x,y in zip(ch2,ch3)]

print("first: ", cht[0])
print("last:  ", cht[-1])

plt.plot(cht,ch0)
plt.show()
plt.plot(cht,ch1)
plt.show()
plt.plot(cht,ch2)
plt.show()
plt.plot(cht,ch3)
plt.show()
