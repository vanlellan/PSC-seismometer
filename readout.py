#!/usr/bin/python
# -*- coding:utf-8 -*-


import time
import ADS1256
import RPi.GPIO as GPIO


try:
    ADC = ADS1256.ADS1256()
    ADC.ADS1256_init()

    with open("seismo.txt","a") as data:

        while(1):
            adc0 = ADC_Value[0]*5.0/0x7fffff
            adc1 = ADC_Value[1]*5.0/0x7fffff
            adc2 = ADC_Value[2]*5.0/0x7fffff
            adc3 = ADC_Value[3]*5.0/0x7fffff
            data.write(adc0,",", adc1,",", adc2,",", adc3,",","\n")
            ADC_Value = ADC.ADS1256_GetAll()
        print ("diff 0-1 = %lf V"%((ADC_Value[0]-ADC_Value[1])*5.0/0x7fffff))
        print ("diff 2-3 = %lf V"%((ADC_Value[2]-ADC_Value[3])*5.0/0x7fffff))
        print ("\33[3A")

        
except :
    GPIO.cleanup()
    print ("\r\nProgram end     ")
    exit()
