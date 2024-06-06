#demonstrate splitting data into sequential files

import time

maxFileLength = 100

while(1):
    with open("demodata"+str(int(time.time()))+".txt",'a') as f:
        for i in range(maxFileLength):
            time.sleep(0.1)
            f.write(str(time.time())+'\n')
