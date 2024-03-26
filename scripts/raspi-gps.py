import datetime
from enum import Enum
from gpiozero import Button, LED, RGBLED
import gpxpy
import math
import os
import serial
import sys
import time

class Color(Enum):
  RED = (0, 1, 1)
  GREEN = (1, 0, 1)
  BLUE = (1, 1, 0)
  NONE = (1, 1, 1)

class Recorder:
  def __init__(self):
    self.recording = False
    self.__file_name = datetime.datetime.now().strftime('%Y%m%dT%H%M%S') + '.gpx'
    # GPX object, track, segment
    self.__gpx = gpxpy.gpx.GPX()
    self.__gpx.name = 'Raspberry Pi GPS'
    self.__gpx.description = 'GPS track'
    self.__gpx_track = gpxpy.gpx.GPXTrack()
    self.__gpx.tracks.append(self.__gpx_track)
    self.__gpx_segment = gpxpy.gpx.GPXTrackSegment()
    self.__gpx_track.segments.append(self.__gpx_segment)

  def addPoint(self, latitude, longitude, elevation, time):
    self.__gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(
      latitude = latitude, 
      longitude = longitude, 
      elevation = elevation, 
      time = time))
    self.write()

  def write(self):
    file = open(self.__file_name, 'w')
    file.write(self.__gpx.to_xml())
    file.close()

def nmeaToDeg(v):
  y, x = math.modf(v / 100)
  y = (y * 10) / 6
  return x + y

def terminate():
  led.color = Color.RED.value
  time.sleep(2)
  led.color = Color.NONE.value
  power.off()
  sys.exit(1)

def shutdown():
  track.write()
  led.color = Color.NONE.value
  power.off()
  os.system('sudo shutdown now')

# button connected to GPIO3
button = Button(3)
# LED pins: red GPIO17, green GPIO22, blue GPIO10
led = RGBLED(red = 17, green = 22, blue = 10)
# power pin on GPIO27
power = LED(27)
power.on()
led.color = Color.BLUE.value

# from argument set sleep
if len(sys.argv) > 1:
  time.sleep(int(sys.argv[1]))

try:
  fp = os.popen('sudo rfcomm bind /dev/rfcomm1 <YOUR_BLUETOOTH_MAC_ADDRESS>')
  time.sleep(2)
  fp.close()
except:
  print(sys.exc_info())
  terminate()

try:
  sr = serial.Serial('/dev/rfcomm1', timeout=2)
except:
  terminate()

led.color = Color.NONE.value
line = ''

t0 = None
lat0 = 0
lon0 = 0
tb0 = None
statusChanged = False
track = Recorder()

while True:
  try:
    if button.is_pressed:
      tb1 = datetime.datetime.now()
      if tb0 == None:
        tb0 = tb1
      td = (tb1 - tb0).total_seconds()
      if td > 10:
        led.color = Color.RED.value
        time.sleep(2)
        shutdown()
      else:
        if td < 0.5:
          # green for start recording, red for stop
          if track.recording:
            led.color = Color.RED.value
          else:
            led.color = Color.GREEN.value
        else:
          if not statusChanged:
            statusChanged = True
            if track.recording:
              track.write()
              track.recording = False
            else:
              track = Recorder()
              track.recording = True
            led.color = Color.NONE.value
    else:
      if tb0 != None:
        tb0 = None
        statusChanged = False
        led.color = Color.NONE.value

    chr = sr.read().decode('utf-8')
    if chr == '\r':
      parts = line.replace('\n', '').split(',')

      try:
        # GGA - Global Positioning System Fix Data
        if parts[0] == '$GPGGA':
          latitude = nmeaToDeg(float(parts[2]))
          latitudeDirection = parts[3]
          longitude = nmeaToDeg(float(parts[4]))
          longitudeDirection = parts[5]
          print('Latitude / longitude: %s %s, %s %s' % 
            (latitude, latitudeDirection, longitude, longitudeDirection))
          elevation = float(parts[9])
          print('Elevation: %s m' % (elevation))
          if track.recording:
            if t0 == None:
              t0 = datetime.datetime.now()
            else:
              t1 = datetime.datetime.now()
              # record every 10 seconds
              if (t1 - t0).total_seconds() > 10 and lat0 != latitude and lon0 != longitude:
                led.color = Color.GREEN.value
                t0 = t1
                lat0 = latitude
                lon0 = longitude
                if latitudeDirection == 'S':
                  latitude = latitude * (-1)
                if longitudeDirection == 'W':
                  longitude = longitude * (-1)
                track.addPoint(
                  latitude = latitude, 
                  longitude = longitude, 
                  elevation = elevation, 
                  time = t1)
                led.color = Color.NONE.value
          else:
            t0 = None
            lat0 = 0
            lon0 = 0

        # VTG - Track made good and Ground speed
        #if parts[0] == '$GPVTG':
        #  speed = float(parts[7])
        #  print('Speed: %s km/h' % (speed))
      except:
        led.color = Color.RED.value
        time.sleep(0.1)
        led.color = Color.NONE.value
        time.sleep(0.5)

      line = ''
    else:
      line = line + chr
  except:
    print(sys.exc_info())
    terminate()
