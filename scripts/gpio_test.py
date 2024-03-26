import datetime
from gpiozero import Button, LED, RGBLED
import time

button = Button(3) # GPIO3
led = RGBLED(red = 17, green = 22, blue = 10) # red GPIO17, green GPIO22, blue GPIO10
power = LED(27) # GPIO27

power.on()
led.color = (0, 1, 1)
print('red')
time.sleep(2)
led.color = (1, 0, 1)
print('green')
time.sleep(2)
led.color = (1, 1, 0)
print('blue')
time.sleep(2)
led.color = (1, 1, 1)

t0 = 0

while True:

  if button.is_pressed:
    print('pressed')
    t1 = datetime.datetime.now()
    if t0 == 0:
      t0 = t1
    if (t1 - t0).total_seconds() > 5:
      led.color = (0, 1, 1)
      print('red')
      time.sleep(1)
      led.color = (1, 1, 1)
      t0 = 0
    else:
      led.color = (0, 0, 1)
      print('yellow')
      time.sleep(1)
      led.color = (1, 1, 1)
  else:
    t0 = 0
    led.color = (1, 0, 1)
    print('green')
    time.sleep(1)
    led.color = (1, 1, 1)

  try:
    time.sleep(1)

  except:
    print(sys.exc_info())
    led.color = (0, 1, 1)
    print('red')
    time.sleep(2)
    led.color = (1, 1, 1)
    power.off()
    sys.exit(1)
