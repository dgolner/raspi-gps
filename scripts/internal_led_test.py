import datetime
from gpiozero import Button
import os
import time

button = Button(3) # GPIO3

os.system('sudo sh -c "echo 1 > /sys/class/leds/mmc0/brightness"')
time.sleep(2)
os.system('sudo sh -c "echo 0 > /sys/class/leds/mmc0/brightness"')

t0 = 0

while True:

  if button.is_pressed:
    print('pressed')
    t1 = datetime.datetime.now()
    if t0 == 0:
      t0 = t1
    if (t1 - t0).total_seconds() > 5:
      os.system('sudo sh -c "echo 1 > /sys/class/leds/mmc0/brightness"')
      time.sleep(1)
      os.system('sudo sh -c "echo 0 > /sys/class/leds/mmc0/brightness"')
      t0 = 0
  else:
    t0 = 0

  time.sleep(1)
