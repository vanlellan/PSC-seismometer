#!/usr/bin/python
# -*- coding:utf-8 -*-


import time as t
import ADS1256
import RPi.GPIO as GPIO


try:
    ADC = ADS1256.ADS1256()
    ADC.ADS1256_init()

    with open("seismo.txt","a") as data:
        adcV = [0.0,0.0,0.0,0.0,0.0]
        while(1):
            t.sleep(0.5)
            ADC_Value = ADC.ADS1256_GetAll()
            adcV[0] = ADC_Value[0]*5.0/0x7fffff
            adcV[1] = ADC_Value[1]*5.0/0x7fffff
            adcV[2] = ADC_Value[2]*5.0/0x7fffff
            adcV[3] = ADC_Value[3]*5.0/0x7fffff
            adcV[4] = t.time()
            print(adcV)
            data.write(str(adcV)+'\n')
            print ("time = %lf"%(adcV[4]))
            print ("diff 0-1 = %lf V"%((ADC_Value[0]-ADC_Value[1])*5.0/0x7fffff))
            print ("diff 2-3 = %lf V"%((ADC_Value[2]-ADC_Value[3])*5.0/0x7fffff))
            print ("\33[5A")

        
except :
    GPIO.cleanup()
    print ("\r\nProgram end     ")
    exit()
