English ∙ [Hrvatski](README-hr.md)

# raspi-gps

This simple project **raspi-gps** is a small GPS tracking system I made using Raspberry Pi and an external GPS Bluetooth module. This device is conceived as offline tracking, just connect it to a USB in the car, turn it on and record movement without connecting to the Internet. Since the movement (change of GPS position in time) is recorded in the form of GPX files on the SD card, it's possible to load such routes in external applications such as Google Earth by downloading from the SD card.

The project seemed interesting to me to share, so I created this tutorial.


## Contents of the project and tutorial

- [Motivation for this project](#motivation-for-this-project)
- [Components](#components)
- [Initial configuration of Raspberry Pi](#initial-configuration-of-raspberry-pi)
- [Raspberry Pi pairing and connecting to Bluetooth GPS module](#raspberry-pi-pairing-and-connecting-to-bluetooth-gps-module)
- [Python communication with Bluetooth GPS module](#python-communication-with-bluetooth-gps-module)
- [GPS codes](#gps-codes)
- [How to create a GPX file](#how-to-create-a-gpx-file)
- [Start a Python script automatically](#start-a-python-script-automatically)
- [Using button and RGB LED](#using-button-and-rgb-led)
- [Python code completion](#python-code-completion)
- [Project in practice](#project-in-practice)
- [Off-topic simplification with fewer components](#off-topic-simplification-with-fewer-components)
- [References](#references)


## Motivation for this project

Raspberry Pi is cool for personal projects and researching what can it do, so after some projects I did with Arduino, I went to something more powerful and more serious. Especially when it starts to think of gadgets that will use Wi-Fi with Bluetooth and program it in Python. From previously collected components in drawers, why not use what I have? I specifically have an old Raspberry Pi Zero W, an even older external GPS device, some electronic components from the starter kits and the idea.

I wanted to make a GPS tracker, but a little different one. The GPS module is not a classic Raspberry Pi component that connects to Raspberry pins. It's an external module with a battery and I can put it in a place where the GPS signal is stronger. That is why there are some advantages over GPS and tracking through cell phones and some special apps. So Raspberry Pi just connects to a USB or Power Bank, merges with GPS, finds visible satellites and starts tracking the position. It's a good idea to save routes on weekend rides. Online monitoring of such a route or current position can only be an upgrade over this project one day.


## Components

For this project, I'll use a Raspberry Pi Zero W just because I have it from before and it's compact enough for me. Any Raspberry that supports Wi-Fi and Bluetooth can be used. Wi-Fi is essential for connection to the PC, configuring, uploading Python code and downloading files from the SD card.

Bluetooth is used to connect to the external GPS module. In my case, I use ancient Haicom HI-406BT, so it's good to keep track of that mark in the tutorial in the part that refers to Bluetooth connection and communication. Almost every standalone Bluetooth GPS device that supports serial communication and NMEA data will serve a purpose. It doesn't matter if it's a premium model (I didn't try Garmin GLO 2 since it's too expensive for my needs) or some cheap noname (an even better option), it's important to find some that can be connected to PC, mobile phone or something third that supports Bluetooth, can pair and support serial communication. Support for Galileo or GLONASS doesn't matter, GPS support is essential, and for easier check of your device just see if it contains at least a SiRF StarIII chip.

Not necessary, but a Power Bank can be connected to Raspberry's USB port if it will not be suited otherwise, eg through USB in the car. Of the other components, there are some resistors, DuPont wires, connectors, a button, RGB LED and a small experimental breadboard, all for the compactness of the solution. The resistors are there for protection and can be of other resistance, not too big and will work OK.

 Components are listed in the table:

| **Used components** |
|---|
| 1x Raspberry Pi Zero W |
| 1x external Bluetooth GPS module |
| 1x powerbank |
| 1x mini breadboard |
| 1x button |
| 1x RGB LED |
| 1x 1 kΩ resistor |
| 2x 10 kΩ resistor |
| pin connectors and DuPont wires |

For the project, I used an RGB LED with a common anode (+ pole), which made it difficult for me to program, but that's the RGB LED that I had. Programming is easier with an LED with a common cathode (- pole). It's easier because the colors are turned on by releasing electricity on each pin in charge of color, for example, high on the red and low on others results only in the red color of the LED. When the LED has a common anode (+), colors are turned on by shutting down the current (sending low on pins), so it's inverted. For example, for red color, it means low on the pin for red and high on the others. If you have an RGB LED that is not like in my case, feel free to play a little for the results.

How the components are first drawn and interconnected on the diagram:

![alt text](/images/Raspberry_Pi_Bluetooth_GPS_full.png "Fritzing diagram - Raspberry Pi Zero W with components")

I use a 1 kΩ resistor on the red pin of the RGB LED while I use 10 kΩ resistors on the others. There is a resistor of lower value on the red to get better light intensity but feel free to play with the combinations of resistors.

This is how the components are connected in the project while still on the table:

[![](/images/assembled_parts1_small.png)](/images/assembled_parts1.png)

[![](/images/assembled_parts2_small.png)](/images/assembled_parts2.png)

After configuring, uploading Python code, local testing and packaging into a small case this is how my project looks in the car connected to a USB and the GPS device is located under the rear glass for a better reception of the satellites:

[![](/images/devices_car_small.png)](/images/devices_car.png)

I made a cardboard mini case, so it can be downloaded, printed and cut, and fits the dimensions of the components I used.

[![Download Icon]](/resources/RasPiGPS_cardboard.pdf)

Once the components are connected, it's necessary to configure the Raspberry Pi before programming.


## Initial configuration of Raspberry Pi

The Raspberry Pi OS has to be installed on the Raspberry Pi that will be used, I installed it over the Raspberry Pi Imager earlier, so it's not covered in this tutorial. It was also created when installing a **pi** user with a password. I don't use Raspberry when it's connected to the monitor, I configured it in headless mode. This can only complicate the work at first. It's important to configure which Wi-Fi network it connects to and which will be a fixed IP address.

To connect to Raspberry over the home Wi-Fi network, it's necessary on its SD card in the root directory to create an empty file **ssh** without extension:

![alt](/images/empty_ssh_file.png)

Also on the SD card in the root directory create a file with the exact name **wpa_supplicant.conf** in which the Wi-Fi connection data will be stored. The contents of the file itself should be:
```sh
country=YOUR_COUNTRY_CODE
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
network={
    ssid="YOUR_WIFI_SSID"
    psk="YOUR_WIFI_PASSWORD"
    key_mgmt=WPA-PSK
}
```

Under **YOUR_COUNTRY_CODE** put your country code (eg us), under **YOUR_WIFI_SSID** put SSID of home Wi-Fi and in **YOUR_WIFI_PASSWORD** put your network password. It's obvious here that security is not at a high level, but at least Raspberry will connect automatically to the network after boot. The next thing after booting is finding its IP address, which can be found most often by connecting and checking on a home router.

The next step is to connect through its IP address using **Putty**, simply entering the SSH connection with the IP address of Raspberry Pi and when requested enter username and password. After connecting, you'll get the shell:

![alt](/images/putty_bash.png)

From the shell, launch the configuration of Raspberry Pi OS:
```sh
sudo raspi-config
```

The Configuration Tool screen is obtained and be sure to set an autologin with user **pi** (set default user) for later automatic launch of the Python script of this project:

![alt](/images/raspi_config1.png)

Also, be sure to enable SSH Server:

![alt](/images/raspi_config2.png)

After leaving the raspi-config, it's necessary to set a static IP address so we don't have to look for it each time Raspberry connects to the router. For this, edit the file **/etc/dhcpcd.conf**, from various shell editors, I mostly use **pico**:
```sh
pico /etc/dhcpcd.conf
```

In the file, you need to locate the section where the static IP address is configured. Initially, all lines in the file are commented out with **#**. Uncomment the lines, following the example, and modify them according to your router’s address and the desired fixed IP address:
```sh
# Example static IP configuration:
interface eth0
static ip_address=<YOUR_RASPBERRY_IP>/24
#static ip6_address=fd51:42f8:caae:d92e::ff/64
static routers=<YOUR_ROUTER_IP>
static domain_name_servers=<YOUR_ROUTER_IP> 8.8.8.8
```
Replace **<YOUR_RASPBERRY_IP>** with the desired fixed address. It can even be the one under which the Raspberry initially connected to the router automatically. Replace **<YOUR_ROUTER_IP>** with the router’s IP address, such as 192.168.0.1 (which remains unchanged). Save the changes and exit the editor.

After making the changes, restart the Raspberry:
```sh
sudo shutdown -r now
```

To upload and download files (Python code, GPX files) on the Raspberry’s SD card while it’s connected to the network, it’s best and most practical to use the FTP protocol along with a free client like FileZilla. To achieve this, follow these steps for installing the FTP server from the shell:
```sh
sudo apt install vsftpd
```

After installation, proceed with configuring the FTP server by editing the file **/etc/vsftpd.conf**:
```sh
sudo pico /etc/vsftpd.conf
```

In the file, when you find these commented lines, uncomment them by removing the **#**
```sh
#write_enable=YES
#local_umask=022
#anon_upload_enable=YES
```

At the end of the file add the following lines:
```sh
user_sub_token=$USER
local_root=/home/$USER/FTP
```

Save changes, exit the editor and from shell create FTP shared directory **FTP/share** in your user home directory and add all rights to users:
```sh
mkdir -p /home/pi/FTP/share
chmod 777 /home/pi/FTP/share
```

Restart FTP daemon:
```sh
sudo service vsftpd restart
```

If everything is successful, you can connect to your Raspberry with an FTP client.


## Raspberry Pi pairing and connecting to Bluetooth GPS module

After the initial configuration, the GPS module checking and pairing with Raspberry Pi is followed and this step is crucial for going on. In the booting sequence of the Raspberry, Bluetooth service is also being launched, so the service status can be checked through the shell command:
```sh
systemctl status bluetooth
```

An active Bluetooth service is expected as in this example:
```sh
● bluetooth.service - Bluetooth service
     Loaded: loaded (/lib/systemd/system/bluetooth.service; enabled; vendor pre>
     Active: active (running) since Mon 2023-11-06 20:23:24 CET; 6 days ago
       Docs: man:bluetoothd(8)
   Main PID: 451 (bluetoothd)
     Status: "Running"
      Tasks: 1 (limit: 724)
        CPU: 327ms
     CGroup: /system.slice/bluetooth.service
             └─451 /usr/libexec/bluetooth/bluetoothd
```

After we checked and confirmed that the service is active now, it's necessary to start scanning for Bluetooth devices nearby. Of course, an external Bluetooth GPS device must be turned on. Finding devices nearby from the shell:
```sh
hcitool scan
```

The result of scanning should be a list of visible Bluetooth devices with their addresses and names, eg:
```sh
pi@raspberrypi:~ $ hcitool scan
Scanning ...
        00:02:78:19:70:30       HI-406BT
        4C:31:2D:73:88:88       MiTV-AYFR0
```

The use of **hcitool** is optional (it's good for control) because I'll continue with interactive tool **bluetoothctl** for pairing and scanning from the shell:
```sh
bluetoothctl
```

After starting, his interactive shell will appear through which the devices are managed:
```sh
Agent registered
[CHG] Controller B8:27:EB:F6:C0:3F Pairable: yes
[bluetooth]#
```

First "power on" Bluetooth from the tool:
```sh
[bluetooth]# power on
Changing power on succeeded
```

Register its agent:
```sh
[bluetooth]# agent on
Agent is already registered
```

Switch to a default agent:
```sh
[bluetooth]# default-agent
Default agent request successful
```

The previous steps were "fire and forget" because I just relied on the methods that surely worked. This is followed by scanning of the surrounding devices and monitoring what will appear as results (visible also through the previous use of **hcitool**):
```sh
[bluetooth]# scan on
Discovery started
[CHG] Controller B8:27:EB:F6:C0:3F Discovering: yes
[NEW] Device DB:93:F3:DA:E4:C0 vívoactive3
[NEW] Device 00:02:78:19:70:30 00-02-78-19-70-30
[CHG] Device 00:02:78:19:70:30 LegacyPairing: no
[CHG] Device 00:02:78:19:70:30 Name: HI-406BT
[CHG] Device 00:02:78:19:70:30 Alias: HI-406BT
[CHG] Device 00:02:78:19:70:30 LegacyPairing: yes
```

From the upper result, it's necessary to find the address of the Bluetooth GPS module according to its name and it's good to remember since it will be used several times throughout the tutorial. It's crucial to detect which GPS module you use since each is different. In my example from the components I used, I found 00:02:78:19:70:30 which corresponds to the name HI-406BT. So, in your case, find which address matches your device and pair it with the command **pair** followed by the address, this is my example:
```sh
[bluetooth]# pair 00:02:78:19:70:30
Attempting to pair with 00:02:78:19:70:30
[CHG] Device 00:02:78:19:70:30 Connected: yes
Request PIN code
[agent] Enter PIN code: 0000
[DEL] Device DB:93:F3:DA:E4:C0 vívoactive3
[CHG] Device 00:02:78:19:70:30 UUIDs: 00001101-0000-1000-8000-00805f9b34fb
[CHG] Device 00:02:78:19:70:30 ServicesResolved: yes
[CHG] Device 00:02:78:19:70:30 Paired: yes
Pairing successful
[CHG] Device 00:02:78:19:70:30 ServicesResolved: no
[CHG] Device 00:02:78:19:70:30 Connected: no
```

Immediately after attempting to pair, as seen above, you will need to enter your **PIN** pairing code, my example and a lot of them by default have **0000**. If everything has passed successfully you will see the message **Pairing successful**. When pairing, it's also possible to get this type of error:
```sh
[bluetooth]# pair 00:02:78:19:70:30
Attempting to pair with 00:02:78:19:70:30
Failed to pair: org.bluez.Error.AlreadyExists
```

> :warning: In this case, the most common problem is that the device is already connected to something and in use, so it needs to be disconnected from this other device. After that, repeat the upper steps. If that doesn't help, restarting of the Bluetooth service could help.

If everything has gone through so far, it's possible to get info about the device and status according to its address:
```sh
[bluetooth]# info 00:02:78:19:70:30
Device 00:02:78:19:70:30 (public)
        Name: HI-406BT
        Alias: HI-406BT
        Class: 0x00001f00
        Paired: yes
        Trusted: no
        Blocked: no
        Connected: no
        LegacyPairing: yes
        UUID: Serial Port               (00001101-0000-1000-8000-00805f9b34fb)
        RSSI: -35
```

Furthermore, all paired devices can be seen, most important is to see the GPS module that will be used in the project:
```sh
[bluetooth]# paired-devices
Device 00:02:78:19:70:30 HI-406BT
```

Finally, since everything went OK, you should exit from the **bluetoothctl** tool because it will no longer be needed:
```sh
[bluetooth]# exit
```

The next step is tool **rfcomm** also used in Bluetooth configuration through shell:
```sh
rfcomm
```

The result will be the address and status of **RFCOMM** channels to which the Bluetooth device is connected as my example:
```sh
rfcomm1: 00:02:78:19:70:30 channel 1 closed
```

It's important to remember the results from **rfcomm1** as it will be used below as part of the command. To connect to the device from the shell, it's necessary to combine **/dev/rfcomm1** and the address of the device from the previous steps:
```sh
rfcomm bind /dev/rfcomm1 00:02:78:19:70:30
```

> :warning:  If you have no rights, the following error will appear:

**Can't create device: Operation not permitted**

The solution is to use **sudo** to call the command:
```sh
sudo rfcomm bind /dev/rfcomm1 00:02:78:19:70:30
```

If we have successfully done all of these steps so far, which means we have already paired the device and we use it, we will get the following message that means everything is OK:
**Can't create device: Address already in use**

It looks like a warning or an error, but it's the result of the previous tools that are used. Later, that binding through **rfcomm1** will be used in Python scripts.


## Python communication with Bluetooth GPS module

It's time to write the first Python program that will communicate with the Bluetooth GPS module. The minimum version of Python should be 3.5, in my case it was used 3.9.2, but it's always good to use the higher version. Since communication through Bluetooth is a serial, first from shell check if there is a Python library **pyserial** that will be used:
```sh
pip3 list | grep pyserial
```

If the upper check doesn't return that the library exists, you should install it (if it shows an error with permissions, switch to **pi** user with **su pi**):
```sh
pip3 install pyserial
```

Now create a new Python file named **raspi-gps.py** that will read serial communication and print as meaningfully as possible. The serial communication reads data from the port located on device **/dev/rfcomm1** which corresponds to the previous chapter. It's important to know that this port will be further used, and the steps for connecting to Bluetooth from the previous chapter are also important. For this first script, it's mandatory to first connect to the GPS module before starting (see previous use of **rfcomm bind**). In an infinite loop, the script is trying to read character by character from the serial port until **'\r'** is found and then, that message is printed. Source code of this first iteration of connecting to the GPS module and serial communication:
```python
import serial

sr = serial.Serial('/dev/rfcomm1', timeout=2)
line = ''

while True:
  chr = sr.read().decode('utf-8')
  if chr == '\r':
    print(line)
    line = ''
  else:
    line = line + chr
```

After a short study of the source code, run it from the shell:
```sh
python3 raspi-gps.py
```

If everything went OK from the previous steps and there were no errors when running the Python script, the cryptic lines similar to my example should soon appear:
```sh
$GPVTG,202.93,T,,M,0.05,N,0.1,K,N*0C

$GPGGA,165941.553,4553.9397,N,01650.9875,E,1,03,2.6,-41.4,M,41.4,M,,0000*49

$GPRMC,165941.553,A,4553.9397,N,01650.9875,E,0.10,216.49,130923,,,A*62

$GPVTG,216.49,T,,M,0.10,N,0.2,K,N*09

$GPGGA,165942.553,4553.9396,N,01650.9875,E,1,03,2.6,-41.4,M,41.4,M,,0000*4B

$GPRMC,165942.553,A,4553.9396,N,01650.9875,E,0.09,252.51,130923,,,A*61

$GPVTG,252.51,T,,M,0.09,N,0.2,K,N*08

$GPGGA,165943.553,4553.9396,N,01650.9874,E,1,03,2.6,-41.4,M,41.4,M,,0000*4B

$GPRMC,165943.553,A,4553.9396,N,01650.9874,E,0.10,215.45,130923,,,A*6F

$GPVTG,215.45,T,,M,0.10,N,0.2,K,N*06
```

This looks completely correct and it's **NMEA** data coming from communication with the GPS module. Further, we'll deal with deciphering these data.

If an error occurs after starting this script and it's related to binding to the GPS module and is also visible as a Python exception, it means that it's necessary to restart the binding before starting this script from the shell. As in the previous steps you must run **rfcomm bind** with the device address (I'll continue to use **<YOUR_BLUETOOTH_MAC_ADDRESS>**) and check the status:
```sh
sudo rfcomm bind /dev/rfcomm1 <YOUR_BLUETOOTH_MAC_ADDRESS>
rfcomm
```

In order not to have to repeat the binding at each launch of Raspberry Pi and check the status before the start of a Python script, I added a call for binding immediately in the script. It will execute the binding by calling an OS command at each start of this script:
```python
import os
import serial
import sys
import time

try:
  fp = os.popen('sudo rfcomm bind /dev/rfcomm1 <YOUR_BLUETOOTH_MAC_ADDRESS>')
  time.sleep(2)
  fp.close()
except:
  print(sys.exc_info())
  sys.exit(1)

try:
  sr = serial.Serial('/dev/rfcomm1', timeout=2)
except:
  sys.exit(1)

line = ''

while True:
  try:
    chr = sr.read().decode('utf-8')
    if chr == '\r':
      print(line)
      line = ''
    else:
      line = line + chr
  except:      
    sys.exit(1)
```

Run again from the shell:
```sh
python3 raspi-gps.py
```

The result should be the same, the **NMEA** data of the GPS module will appear and less should be taken care of connecting to the module, it's enough to turn it on and after that, you can run the Python script that will begin to communicate with it.


## GPS codes

**NMEA** (National Marine Electronics Association) is as it says an association, and for is important **NMEA-0183** communication specification primarily intended for nautical electronics. Most importantly, it's used as a standard for communication with GPS devices. External GPS devices receive signals from visible satellites and form NMEA data that transmit further as in our case via Bluetooth serial communication. The data contain the talker ID (GPS, Galileo, GLONASS, BeiDou), message group and the data that correspond to the group. Details of the groups and message content with field descriptions are available in the link [NMEA Sentences](https://receiverhelp.trimble.com/alloy-gnss/en-us/NMEA-0183messages_MessageOverview.html).

Any message that is received (NMEA sentence) begins with **$** and talker ID, from the above example comes **$GP** which is a label for **GPS**. If your GPS module supports other systems, you could also get the start of a message for example with $GA as Galileo. I'll focus on GPS so I'll decode messages that start with **$GP**. After the talker ID comes the message group, and for this project, the most important are the **GGA - Global Positioning System Fix Data** and **VTG - Track made good and Ground speed**. GGA data contain various fields that are important to me: latitude, longitude, elevation and orientation, I won't use others. VTG is interesting to me just for reading the speed, I don't use the rest.

I extracted the necessary information according to the group and filed position in the message, it helped me NMEA documentation, and further, all that matters is the presentation of the data. There is a challenge with the value of the latitude and longitude because their values are slightly different from expectations, so it's necessary to convert from NMEA formatted data (format is (d)ddmm.mmmm where **d** stands for degrees, and **m** stands for minutes) to decimal format. I used a little help from an article on [Stack Overflow](https://stackoverflow.com/questions/36254363/how-to-convert-latitude-and-longitude-of-nmea-format-data-to-decimal) so I also created a conversion function in my Python code.

I've upgraded the upper Python code for reading the NMEA data. Every message that is read from GPS, regarding NMEA codes is extracted and checked if it contains the necessary GGA and VTG groups and the necessary values in them. To display the position, I additionally convert values to degrees and add the orientation. So upgraded and beautified Python source code looks now like this:
```python
import math
import os
import serial
import sys
import time

def nmeaToDeg(v):
  y, x = math.modf(v / 100)
  y = (y * 10) / 6
  return x + y

try:
  fp = os.popen('sudo rfcomm bind /dev/rfcomm1 <YOUR_BLUETOOTH_MAC_ADDRESS>')
  time.sleep(2)
  fp.close()
except:
  print(sys.exc_info())
  sys.exit(1)

try:
  sr = serial.Serial('/dev/rfcomm1', timeout=2)
except:
  sys.exit(1)

line = ''

while True:
  try:
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

        # VTG - Track made good and Ground speed
        if parts[0] == '$GPVTG':
          speed = float(parts[7])
          print('Speed: %s km/h' % (speed))
      except:
        None

      line = ''
    else:
      line = line + chr
  except:
    print(sys.exc_info())
    sys.exit(1)
```

Run again from the shell:
```sh
python3 raspi-gps.py
```

The result should be a formatted output print of the current GPS position, elevation and speed if it's all successfully read.


## How to create a GPX file

After launching and testing this program, the next step is writing GPS positions in a file, we'll specifically use **GPX** format. **GPX** ([GPS Exchange Format](https://en.wikipedia.org/wiki/GPS_Exchange_Format)) is an XML schema for GPS data recording that can be used in other applications, and in this tutorial, we'll use it to write down the track. This results in the tracking of our Raspberry Pi device. The new unique **.gpx** file will always be created when launching the Python script. The reason for recording the change of location, and only if it occurs after 10 seconds is a reduction of file size, there is no need to write down the same position in the file or just any minimum change. These parameters can be manipulated, it just takes a small modification of the script.

To create **GPX** format in Python we will use the library **gpxpy** - [GPX File Parser](https://pypi.org/project/gpxpy/). First, you need to check if the library is installed:
```sh
pip3 list | grep gpxpy
```

If the upper check doesn't return the existence of the library (initially it's not installed), you should install it (if an error occurs that there are no user rights, switch to **pi** user with **su pi**) from the shell:
```sh
pip3 install gpxpy
```

The use of this library consists of creating an object and its tracks and segments containing points. Point is a single GPS position that we'll add to an object which we'll save in the GPX file. Since the position in the GPX object cannot be written exactly how we read it from communication and its NMEA messages, it needs to be adjusted a little bit. One step of adjustment is the very formatting of the position as I did it in the previous Python script, so I'll use it, followed by another addition. The orientation of the position (N, S, E, W) is a single field in the NMEA message, but in the GPX format, it's contained in geographical latitude and longitude. Therefore, orientations S and W are multiplied with -1 to convert them into GPX format. Also, an important thing is to write the exact time that must be in **ISO 8601** format.

In the below code, it can be seen that the script doesn't record speed in the GPX object. The reason is that by default, GPX version 1.1 is used in which speed is not supported. If a speed (for auto enthusiasts) needs to be written, the GPX 1.0 version should be used. That's a smaller adjustment, the speed value should be added to the end of the parameter list of the ```gpxpy.gpx.GPXTrackPoint``` as ```speed = speed``` and method call ```gpx.to_xml()``` should be replaced with ```gpx.to_xml(version="1.0")``` while the rest remains the same. For some can be an additional challenge that speed is read from the VTG message, and the rest of the data from the GGA message which is currently recorded.

The additional tiny functionality I added at the beginning of the Python script at execution refers to the reading of the arguments with which we start it. It can be of good use when preparing for pairing and starting communication with the GPS module. The addition is, that if a number is passed as an argument, the script will pause for so many seconds before continuing to work. This functionality will be used in the next chapter.

The new Python source code after the addition of the described functionalities:
```python
import datetime
import gpxpy
import math
import os
import serial
import sys
import time

def nmeaToDeg(v):
  y, x = math.modf(v / 100)
  y = (y * 10) / 6
  return x + y

# from argument set sleep
if len(sys.argv) > 1:
  time.sleep(int(sys.argv[1]))

try:
  fp = os.popen('sudo rfcomm bind /dev/rfcomm1 <YOUR_BLUETOOTH_MAC_ADDRESS>')
  time.sleep(2)
  fp.close()
except:
  print(sys.exc_info())
  sys.exit(1)

try:
  sr = serial.Serial('/dev/rfcomm1', timeout=2)
except:
  sys.exit(1)

line = ''

# GPX object, track, segment
gpx = gpxpy.gpx.GPX()
gpx.name = 'Raspberry Pi GPS'
gpx.description = 'GPS track'
gpx_track = gpxpy.gpx.GPXTrack()
gpx.tracks.append(gpx_track)
gpx_segment = gpxpy.gpx.GPXTrackSegment()
gpx_track.segments.append(gpx_segment)

t0 = None
lat0 = 0
lon0 = 0
file_name = datetime.datetime.now().strftime('%Y%m%dT%H%M%S') + '.gpx'

while True:
  try:
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
          if t0 == None:
            t0 = datetime.datetime.now()
          else:
            t1 = datetime.datetime.now()
            # record every 10 seconds
            if (t1 - t0).total_seconds() > 10 and lat0 != latitude and lon0 != longitude:
              t0 = t1
              lat0 = latitude
              lon0 = longitude
              if latitudeDirection == 'S':
                latitude = latitude * (-1)
              if longitudeDirection == 'W':
                longitude = longitude * (-1)
              gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(
                latitude = latitude, 
                longitude = longitude, 
                elevation = elevation, 
                time = t1))
              file = open(file_name, 'w')
              file.write(gpx.to_xml())
              file.close()

        # VTG - Track made good and Ground speed
        if parts[0] == '$GPVTG':
          speed = float(parts[7])
          print('Speed: %s km/h' % (speed))
      except:
        None

      line = ''
    else:
      line = line + chr
  except:
    print(sys.exc_info())
    sys.exit(1)
```

Run from the shell:
```sh
python3 raspi-gps.py
```

The result should be the same as in the previous Python code, and in the same directory, it'll also be created **.gpx** file whose size will increase as the GPS position change is recorded.


## Start a Python script automatically

Now the Python script is already completed, so it could be automatically run every time after boot of a Raspberry Pi instead of manually starting. Manual starting is fine when you program locally and test like this, but in real life, it must be automatically run as soon as possible. To add automatic starting after booting, it's necessary to edit the file **/etc/rc.local**, I'll use pico again:
```sh
sudo pico /etc/rc.local
```

It's necessary to position before line **exit 0** and add the following lines:
```sh
cd /home/pi/FTP/share
sudo -u pi python3 raspi-gps.py 30 > log.txt 2>&1 &
```

In my case file now looks like this:

![alt](/images/putty_rc_local.png)

With this change, we are first positioning in the directory where the Python script is located. After that, under the user **pi** (this is required) a Python script **raspi-gps.py** is started with a 30-second waiting parameter (which should be enough to start all the services on which it depends), output messages of the script are forwarded to the log file **log.txt** so that errors can be seen in it, and at the end of the whole row there is a mandatory sign **&** that launches the process in the background.

I mentioned the 30-second waiting parameter in the previous chapter and refers to this part of the Python code, so if another number is passed, for that many seconds it'll wait to continue for execution:
```python
# from argument set sleep
if len(sys.argv) > 1:
  time.sleep(int(sys.argv[1]))
```

After saving the changes of file **/etc/rc.local**, it's necessary to restart Raspberry Pi from the shell:
```sh
sudo shutdown -r now
```
or
```sh
sudo reboot
```

With that and if everything went OK, the Python script will be automatically launched. If errors occurs, they're visible in the same directory in file **log.txt**.

It's also important to mention, that after successfully launching, if we connect to Raspberry Pi with Putty and change the script, before the next start of it, it's necessary to kill the existing process. How to check whether the script is running using the shell:
```sh
ps -fu pi | grep raspi-gps
```

According to the result, just find ```<pid>``` of the active process and from the shell call ```kill <pid>``` of that process.


## Using button and RGB LED

So far, the basis of the GPS tracker has been made, which can be used as it is, but then there is no interaction. It's time to make use of the button which is, in this project the only form of interaction together with RGB LED signaling by Raspberry Pi. For this purpose, we'll create a new Python file **gpio_test.py** which will try to work with the connected button and turn on and off RGB LED in various colors.

We saw the way of connecting the button and RGB LED with the Raspberry Pi at the beginning of the chapter [Components](#components). The components are connected to the Raspberry Pi voltage pin, ground pin and general-purpose pins. Pinout and the purpose of each pin can be seen at the link [Raspberry Pi Pinout](https://pinout.xyz/) or from the shell:
```sh
pinout
```

I chose pins that suit me according to the layout, in your version of the project you can also use some others with some changes in the code. In this testing script, I'll use the **GPIO3** pin to read if the button is pressed, the **GPIO17** pin for the red color of the RGB LED, the **GPIO22** pin for green and the **GPIO10** pin for blue. I will also use the **GPIO27** pin for voltage.

For managing GPIO pins I'll use **gpiozero** interface which should already be installed as part of Python in the Raspberry OS. I'll use its Button, LED and RGBLED classes and each of them will assign management of a particular pin. Programming is relatively simple and intuitive, it consists of turning on / off individual pins or reading the state of a button on the pin. Source code **gpio_test.py** that manages a button and RGB LED looks like this:
```python
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
```
[![Download Icon]][def-gpio_test.py]

After a little studying of what and how this source code works, it should be launched from the shell:
```sh
python3 gpio_test.py
```

In initialization, each class is assigned with individual pins. Immediately for two seconds, the RGB LED should be turned on red, green and blue. How to use the RGBLED class depends on the RGB LED used, I used the one with a common anode (+). In that case, the voltage is released to a single pin that manages the color. After turning on every color from above, the program checks the status of the button, if it's pressed for more than 5 seconds RGB LED will turn on red, shorter than that will turn on yellow, and if the button isn't pressed it will turn on green. After one second, the next iteration of the loop goes. Just in case, the status of a pressed button and which color is turned on will print when running.


## Python code completion

In this chapter, all previous versions of Python scripts are combined in one final Python source code of the project, it's the one that manages the Bluetooth, GPS module, button and RGB LED.

In addition, I'll take the opportunity to abstract some functionalities into classes and add some new functions. I created a new class **Color** as an enumeration for turning on individual colors on RGB LED. I separated creating and writing a route into a new class **Recorder**. For unexpected termination of the program, I further made a function **terminate** and to shut down the Raspberry Pi I made a function **shutdown**. I added a new large block of code for managing the detection of button presses and depending on the length of the pressure the statuses of the start and stop of the route recording are changed with the LED signaling. I also added a new functionality of shutting down the entire Raspberry Pi using the long button press. There is a short user manual under the source code.

The final completed source code of **raspi-gps.py** now looks like this:
```python
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
```
[![Download Icon]][def-raspi-gps.py]

After studying the source code for a bit, it should be launched from the shell, but now because of complexity it's good to check the syntax first as a new step before running:
```sh
python3 -m py_compile raspi-gps.py
python3 raspi-gps.py
```

Now the program will start signaling its work.

RGB LED turns blue for connecting to the GPS module. If an error occurs during this process, the LED turns red for 2 seconds and the program exits with its execution. In that case, there is no other solution than to look at the **FTP/share** directory log to see errors. Such errors should have been also visible earlier during the testing. Otherwise, if everything went OK in the previous steps of the tutorial, further problems are not expected.

When the GPS module has been successfully paired with Raspberry, the program occasionally gives some additional signals. While recording the route if the position changes every 10 seconds, the LED with turn green. If it's not completely positioned towards the satellites and doesn't read the position correctly, it will turn red. Pressing the button while not recording the route, the LED will turn green. Just keep the button pressed for 0.5 seconds to start recording the route. Otherwise, while program records the route, pressing the button will turn red. Holding a button for 0.5 seconds while recording; will stop recording the route. That's why the same button is for on/off mode, so on will turn LED green and off will turn red.

Each recording is saved as a separate **.gpx** file in the directory **FTP/share** and it can be downloaded and opened in a standalone software such as Google Earth for a visual examination of the route. For terminating this Python program, but also shut down the whole Raspberry, it's necessary to keep the button pressed for 10 seconds, which will signal with the LED turned in red. When you want to restart, repeat all the previous steps or physically turn on Raspberry.

And those are the instructions for using it. :smiley:


## Project in practice

After testing the whole system at home and on the PC, it's time to use it in real conditions, in my case in driving one route. By connecting the Raspberry to the car's USB or Power Bank, it starts to boot and then immediately launches the Python script. So when Raspberry boots, it's necessary to immediately turn on the external GPS module for pairing with Bluetooth and try to position it as soon as possible according to visible satellites. After that, it's up to you when to start and stop route recording using the button according to the manual from the previous chapter.

One of my recorded routes is in this example:

[![Download Icon]][def-gpx-sample]

I opened the **.gpx** file in Google Earth and its picture is below. The tool is intuitive enough, so after loading the route and its drawing, some additional buttons on its interface will appear.

[![](/images/Google_Earth_gpx_small.png)](/images/Google_Earth_gpx.png)


## Off-topic simplification with fewer components

If Raspberry Pi Zero W is used as in my case and you want to simplify this project by the reduction of the number of components, the internal LED of Raspberry could be used instead of RGB LED on the breadboard. Further, if you won't use resistors and DuPont wires, you'll end up just connecting the button to Raspberry as in this minimal diagram:

![alt text](/images/Raspberry_Pi_Bluetooth_GPS_simple.png "Fritzing diagram - Raspberry Pi Zero W with minimum set of components")

It looks ascetic and extremely compact, and turning on and off of an internal LED is possible with a little hack of using shell commands. It's about writing high (1) or low (0) values in the file **/sys/class/leds/mmc0/brightness** which is not possible for ordinary users, so we will use **sudo**.

Turning on the internal LED from the shell:
```sh
sudo sh -c "echo 1 > /sys/class/leds/mmc0/brightness"
```
Turning off the internal LED from the shell:
```sh
sudo sh -c "echo 0 > /sys/class/leds/mmc0/brightness"
```
If it fails from the first attempt, just start the commands again from the shell.

How to turn on and off the internal LED with a button and program it as a simple Python script? Below is the implementation that uses shell commands from Python, the calls of sending high and low values are first tried, and then the pressure of the button on the GPIO3 pin is monitored. Holding down the button for 5 seconds turns on the LED for a second and then it turns it off.

Create a new file **internal_led_test.py** with this source code:
```python
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
```
[![Download Icon]][def-internal_led_test.py]

Run this Python script from the shell:
```sh
python3 internal_led_test.py
```

If everything is OK, with a little intervention in source code you can relatively easily upgrade **raspi-gps.py** to make Raspberry work with an internal LED. :yum:


## References

- [Headless Raspberry Pi Setup](https://learn.sparkfun.com/tutorials/headless-raspberry-pi-setup/wifi-with-dhcp)
- [Raspberry Pi Configuration](https://www.raspberrypi.com/documentation/computers/configuration.html)
- [Raspberry Pi Hardware](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html)
- [Raspberry Pi Pinout](https://pinout.xyz/)
- [NMEA Sentences](https://receiverhelp.trimble.com/alloy-gnss/en-us/NMEA-0183messages_MessageOverview.html)
- [GPS Exchange Format](https://en.wikipedia.org/wiki/GPS_Exchange_Format)
- [GPX File Parser](https://pypi.org/project/gpxpy/)
- [Physical Computing with Python](https://projects.raspberrypi.org/en/projects/physical-computing/0)

<!----------------------------------------------------------------------------------------------------------------->

[def-gpio_test.py]: /scripts/gpio_test.py
[def-raspi-gps.py]: /scripts/raspi-gps.py
[def-internal_led_test.py]: /scripts/internal_led_test.py
[def-gpx-sample]: /resources/20231026T195728.gpx

[Download Icon]: https://img.shields.io/badge/Download-37a779?style=for-the-badge&logoColor=white&logo=DocuSign
