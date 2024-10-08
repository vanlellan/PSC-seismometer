#!/usr/bin/python
# -*- coding:utf-8 -*-

import datetime
import time as t
import ADS1256
import RPi.GPIO as GPIO
import traceback


startdate = datetime.date.today()
maxfilelength = 100000 
try:
    ADC = ADS1256.ADS1256()
    ADC.ADS1256_init()
    ADC.ADS1256_SetMode(1)

    while(1):
        with open("/media/psc/USB20FD/"+str(int(t.time()))+".txt","a") as data:
            adcV = [0.0,0.0,0.0,0.0,0.0]
            ADC_Value = ADC.ADS1256_GetAll()    #throw away first readout
            for i in range(maxfilelength):
             #   t.sleep(0.5)
                ADC_Value = ADC.ADS1256_GetAll()
                adcV[0] = ADC_Value[0]*5000.0/0x7fffff  #mV
                adcV[1] = ADC_Value[1]*5000.0/0x7fffff  #mV
                adcV[2] = ADC_Value[2]*5000.0/0x7fffff  #mV
                adcV[3] = ADC_Value[3]*5000.0/0x7fffff  #mV
                adcV[4] = t.time()
                #print(adcV)
                data.write(f"{adcV[0]:.6f},{adcV[1]:.6f},{adcV[2]:.6f},{adcV[3]:.6f},{adcV[4]:.6f}\n")
                print (f"time = {adcV[4]:.4f}")
                print (f"diffadc0 = {(ADC_Value[0])*5000.0/0x7fffff:.6f}")
                print (f"diffadc1 = {(ADC_Value[1])*5000.0/0x7fffff:.6f}")
                print (f"diffadc2 = {(ADC_Value[2])*5000.0/0x7fffff:.6f}")
                print (f"diffadc3 = {(ADC_Value[3])*5000.0/0x7fffff:.6f}")
                print ("\33[6A")

        
except Exception:
    traceback.print_exc()
    GPIO.cleanup()
    print ("\r\nProgram end     ")
    exit()
