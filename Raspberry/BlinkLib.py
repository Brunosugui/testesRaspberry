#!/usr/bin/env python
# coding: utf-8

# In[2]:


import time


# In[3]:


def Blink():
    print("DANGER")
    GPIO.output(led_pin, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(led_pin, GPIO.LOW)
    time.sleep(1)


# In[ ]:




