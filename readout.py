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
            adcV[0] = ADC_Value[0]*5000.0/0x7fffff  #mV
            adcV[1] = ADC_Value[1]*5000.0/0x7fffff  #mV
            adcV[2] = ADC_Value[2]*5000.0/0x7fffff  #mV
            adcV[3] = ADC_Value[3]*5000.0/0x7fffff  #mV
            adcV[4] = t.time()
            #print(adcV)
            data.write(f"{adcV[0]:.3f},{adcV[1]:.3f},{adcV[2]:.3f},{adcV[3]:.3f},{adcV[4]:.3f}\n")
            print (f"time = {adcV[4]:.3f}")
            print (f"diff 0-1 = {(ADC_Value[0]-ADC_Value[1])*5000.0/0x7fffff:.3f}")
            print (f"diff 2-3 = {(ADC_Value[2]-ADC_Value[3])*5000.0/0x7fffff:.3f}")
            print ("\33[4A")

        
except :
    GPIO.cleanup()
    print ("\r\nProgram end     ")
    exit()
