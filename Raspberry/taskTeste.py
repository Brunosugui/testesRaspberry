#!/usr/bin/env python
# coding: utf-8

# In[1]:


import time
from multiprocessing import Process, Manager, Value
import RPi.GPIO as GPIO
import threading


# In[2]:


def handle(pin):
    print("Interrupt from pin " + str(pin))
    print("estado do pino: " + str(GPIO.input(pin)))
    
    if stateGlobal.value == 0:
        stateGlobal.value = 1
    else:
        stateGlobal.value = 0
    print("Interrupt: state global = " + str(stateGlobal.value))


# In[3]:


def gpioSetup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    led_pin = 18
    btn_pin = 17
    GPIO.setup(btn_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(led_pin, GPIO.OUT, initial=GPIO.LOW)
    GPIO.add_event_detect(btn_pin, GPIO.BOTH, handle)


# In[4]:


def thread1(stateGlobal):
    state = True
    while True:
        print("Thread1: state global = " + str(stateGlobal.value))
        if state == True:
            state = False
        else:
            state = True
        GPIO.output(18, state)
        time.sleep(1)


# In[5]:


def task1(state):
    while True:
        print("Task1: state global = " + str(stateGlobal.value))
        time.sleep(1)


# In[6]:


with Manager() as manager:
    gpioSetup()
    
    stateGlobal = Value('d', 0.0)
    print("Starting App...\n")

    t = threading.Thread(target=thread1, args=(stateGlobal,))
    t.daemon = True
    t.start()

    task1 = Process(target=task1, args=(stateGlobal,))

    task1.start()

    print("DONE!")


# In[ ]:




