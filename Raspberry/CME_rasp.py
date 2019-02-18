#!/usr/bin/env python
# coding: utf-8

# In[8]:


import serial
import time
import pandas as pd
from sklearn.externals import joblib
from multiprocessing import Process, Manager, Value
import RPi.GPIO as GPIO
from BlinkLib import Blink


# In[9]:


#blink led
#def Blink():
 #   print("DANGER")
  #  GPIO.output(led_pin, GPIO.HIGH)
   # time.sleep(1)
    #GPIO.output(led_pin, GPIO.LOW)
    #time.sleep(1)


# In[10]:


# processa os dados no formato para o modelo de predicao
def assertAlert(timeDiff, RSSI, lastRSSI):
    data = pd.DataFrame({'RSSI': [RSSI], 'TimeDiff':[timeDiff], 'LastRSSI':[lastRSSI]})
    print(data)
    alert = knn.predict(data)
    if alert == 1:
        state.value = 1
    else:
        state.value = 0


# In[11]:


#processa string esperada no formato:
# TIME; MAC ADDRESS; RSSI\n
def processString(string):
    finalString = string.split(';')
    try:
        Dtime = finalString[0]
        DMAC = finalString[1]
        DRSSI = finalString[2].split('\n')[0]
        return int(Dtime)*100, DMAC, int(DRSSI)
    except:
        return 0


# In[12]:


#read uart line
def readLine(port):
    rv=""
    while True:
        ch = port.read()
        try:
            rv += ch.decode('utf-8')
        except:
            return
        if(ch == b'\r' or ch == b'\n'):
            return rv


# In[13]:


#task para sinalizar
def AssertSignal(state):
    print("Starting Signal assert task:")
    while True:
        if(state.value == 1):
            Blink()
        else:
            print('SAFE')
            time.sleep(1)
    print('signal: DONE!')


# In[14]:


#task para verificacao da UART
def UARTget(state):
    lastTime=0
    lastRSSI=0
    print('Starting UART task...\n')
    while True:
        print('Waiting for message...')
        rcv=readLine(ser)
        Dtime, Dmac, Drssi = processString(rcv)
        if(lastTime != 0 and lastRSSI != 0):
            assertAlert(Dtime-lastTime, Drssi, lastRSSI)
        lastTime = Dtime
        lastRSSI = Drssi
        #print('Time: ' + str(Dtime) + ' MAC: ' + Dmac + ' RSSI: ' + str(Drssi))
    print("uartget: DONE!")


# In[15]:


#Main Code
print("Check if its main")
if __name__ == '__main__':
    with Manager() as manager:
        ser = serial.Serial('/dev/serial0', 115200)
        knn = joblib.load('/home/pi/Desktop/MyScripts/CME_knnModel.sav')
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        led_pin = 18
        GPIO.setup(led_pin, GPIO.OUT, initial=GPIO.LOW)
        state = Value('d', 0.0)
        print("Starting App...\n")
        
        signal = Process(target=UARTget, args=(state,))
        alert = Process(target=AssertSignal, args=(state,), daemon=True)
        
        signal.start()
        alert.start()
        
        print("DONE!")


# In[ ]:




