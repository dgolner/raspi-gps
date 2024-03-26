[English](README.md) ∙ Hrvatski

# raspi-gps

Ovaj jednostavni projekt **raspi-gps** je mali GPS tracking sustav koji sam napravio koristeći Raspberry Pi i eksterni GPS Bluetooth modul. Ovakav uređaj je zamišljen kao offline tracking, odnosno samo se spoji na USB u npr. autu, upali i bilježi se kretanje bez spajanja na Internet. Pošto se kretanje (promjena GPS pozicije u vremenu) bilježi u obliku GPX fileova na SD kartici, po downloadu s SD kartice moguće je takve rute kretanja učitati u vanjsku aplikaciju kao što je Google Earth.

Projekt mi se učinio zanimljivim za podijeliti pa sam iz njega kreirao i daljnji tutorial.


## Sadržaj projekta i tutoriala

- [Motivacija za izradu projekta](#motivacija-za-izradu-projekta)
- [Komponente](#komponente)
- [Inicijalno konfiguriranje Raspberry Pi-ja](#inicijalno-konfiguriranje-raspberry-pi-ja)
- [Raspberry Pi uparivanje i spajanje Bluetooth GPS modula](#raspberry-pi-uparivanje-i-spajanje-bluetooth-gps-modula)
- [Python komunikacija s Bluetooth GPS modulom](#python-komunikacija-s-bluetooth-gps-modulom)
- [GPS kodovi](#gps-kodovi)
- [Kreiranje GPX filea](#kreiranje-gpx-filea)
- [Automatsko pokretanje Python skripte](#automatsko-pokretanje-python-skripte)
- [Korištenje gumba i RGB LED-ice](#korištenje-gumba-i-rgb-led-ice)
- [Kompletiranje Python koda](#kompletiranje-python-koda)
- [Projekt u živom radu](#projekt-u-živom-radu)
- [Off topic pojednostavljenje s manje komponenti](#off-topic-pojednostavljenje-s-manje-komponenti)
- [Reference](#reference)


## Motivacija za izradu projekta

Raspberry Pi je cool za osobne projekte i istraživanje što sve može pa nakon nekih projekata koje sam radio s Arduinom krenuo sam na nešto moćnije i ozbiljnije. Pogotovo kad se krene u smišljanje gadgeta koji će koristiti Wi-Fi, Bluetooth i još k tome sve isprogramirati u Pythonu. Od ranije skupljenih komponenti po ladicama zašto ne iskoristiti ono što imam? Konkretno imam dosta stari Raspberry Pi Zero W, još stariji samostalni eksterni GPS uređaj, nešto elektroničkih komponenti iz starter kitova i ideju.

Želio sam napraviti GPS tracker, ali malo drugačiji. GPS modul nije neki klasičan kao komponenta koja se spaja na pinove Raspberryja nego eksterni s vlastitom baterijom i kojeg mogu staviti na neko mjesto gdje će bolje hvatati GPS signal. Zato ima i neke prednosti pred GPS-om i trackingom preko mobitela i neke posebne aplikacije. Raspberry Pi se onda samo spoji na USB ili powerbank, upali i kad se spoji s GPS-om, ulove vidljivi sateliti praćenje pozicije može započeti. Dobra je primjena spremanje rute na vikend vožnjama. Online praćenje takve rute ili trenutnog položaja može biti samo nadogradnja jednog dana nad ovim projektom.


## Komponente

Za ovaj projekt osnova mi je Raspberry Pi Zero W samo zato što ga imam od prije i što mi je dovoljno kompaktan. Može se koristiti bilo koji Raspberry koji podržava Wi-Fi i Bluetooth. Wi-Fi je bitan zbog spajanja na PC, konfiguriranje, upload Python koda i download fileova s SD kartice.

Bluetooth se koristi za spajanje na eksterni GPS modul. U mom slučaju koristim prastari Haicom HI-406BT pa je dobro pratiti tu oznaku u dijelu tutoriala koji se odnosi na Bluetooth spajanje i komunikaciju. Gotovo svaki samostalni Bluetooth GPS uređaj koji podržava serijsku komunikaciju i NMEA podatke poslužit će svrsi. Nije bitno radi li se o nekom premium modelu (nisam probao Garmin GLO 2 pošto je preskup za moje potrebe) ili nekom jeftinom no name (čak bolja opcija), bitno pronaći neki koji se može spojiti na PC, mobitel ili nešto treće što podržava Bluetooth, može se upariti i podržava serijsku komunikaciju. Nije bitna podrška za Galileo ili GLONASS, bitna je podrška za GPS, a za lakšu provjeru uređaja dovoljno gledati sadrži li najmanje SiRF StarIII čip.

Nije nužan, ali dobro dođe powerbank spojen na Raspberryjev USB port ako se neće drugačije napajati, npr. preko USB-a u autu. Od ostalih komponenti tu je nešto otpornika, žica, konektora, gumb, RGB LED-ica i mala eksperimentalna pločica, isto zbog kompaktnosti rješenja. Otpornici su tu zbog zaštite te mogu biti i nekog drugog otpora, ne prevelikog i radit će ok.

Ugrubo su komponente popisane u tablici:

| **Korištene komponente** |
|---|
| 1x Raspberry Pi Zero W |
| 1x eksterni Bluetooth GPS modul |
| 1x powerbank |
| 1x mini eksperimentalna pločica |
| 1x gumb |
| 1x RGB LED |
| 1x 1 kΩ otpornik |
| 2x 10 kΩ otpornik |
| pin konektori i žice |

Za projekt sam koristio RGB LED-icu sa zajedničkom anodom (+ pol) što mi je malo otežalo programiranje, ali takvu sam imao. Lakše je programiranje kada je takva LED-ica sa zajedničkom katodom (- pol). Lakše je pošto se tada boje pale puštanje struje na pojedini pin zadužen za boju, npr. high na pinu za crvenu i low na ostalima rezultira samo crvenom bojom LED-ice. Kada se radi o zajedničkoj anodi (+), boje se pale zapravo gašenjem struje, odnosno inverzno je. Tako npr. za crvenu boju znači low na pinu za crvenu, a high na ostalim. Ako imate RGB LED-icu koja eto nije kao u mom slučaju slobodno se poigrajte malo za rezultate.

Kako su komponente prvo nacrtane i međusobno spojene na dijagramu:

![alt text](/images/Raspberry_Pi_Bluetooth_GPS_full.png "Fritzing dijagram - Raspberry Pi Zero W s komponentama")

Na crvenom pinu RGB LED-ice koristim otpornik od 1 kΩ dok na drugima koristim 10 kΩ otpornik. Na crvenom je manji zbog dobivanja intenziteta svjetla, ali slobodno se poigrajte s kombinacijama otpornika.

Ovako su stvarno komponente spojene u projektu dok je još na stolu i izradi:

[![](/images/assembled_parts1_small.png)](/images/assembled_parts1.png)

[![](/images/assembled_parts2_small.png)](/images/assembled_parts2.png)

Nakon konfiguriranja, uploada Python koda, lokalnog testiranja i pakiranja u malo vlastito kućište ovako moj projekt izgleda kad se nalazi u autu priključen na USB, a GPS uređaj je smješten ispod stražnjeg stakla radi boljeg prijema satelita:

[![](/images/devices_car_small.png)](/images/devices_car.png)

Samo mini kućište sam izradio iz kartona pa se može preuzeti, isprintati i izrezati, a odgovara dimenzijama mojih korištenih komponenti.

[![Download Icon]](/resources/RasPiGPS_cardboard.pdf)

Nakon što su komponente spojene, prije programiranja potrebno je Raspberry Pi konfigurirati.


## Inicijalno konfiguriranje Raspberry Pi-ja

Na Raspberry Pi-ju koji će se koristiti već mora biti instaliran Raspberry Pi OS, njega sam još od prije instalirao preko Raspberry Pi Imagera pa nije obuhvaćeno tutorialom. Također je na njemu prilikom instalacije kreiran i **pi** user s passwordom. Sam Raspberry inače ne koristim kad je spojen na monitor nego se spajam i konfiguriram u headless modu. To može samo malo komplicirati rad u početku. Bitno mu je složiti na koji se Wi-Fi spaja i koja će mu biti fiksna IP adresa.

Kako bi se moglo na njega spajati preko kućnog Wi-Fija prvo je potrebno na njegovoj SD kartici u rootu kreirati prazan file naziva **ssh** bez ekstenzije:

![alt](/images/empty_ssh_file.png)

Također na SD kartici u rootu kreirati file točnog naziva **wpa_supplicant.conf** u kojem će se popuniti podaci za spajanje na Wi-Fi. Sadržaj samog file treba biti:
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

Pod **YOUR_COUNTRY_CODE** staviti oznaku države (meni HR), pod **YOUR_WIFI_SSID** staviti SSID kućnog Wi-Fija i u **YOUR_WIFI_PASSWORD** staviti password mreže. Naravno ovdje je očito kako sigurnost nije na razini, ali barem će se Raspberry prilikom bootanja spojiti na mrežu. Sljedeća je stvar nakon što se boota pronaći njegov IP koji je dobio na mreži što se može pronaći najčešće spajanjem i provjerom na kućnom routeru.

Idući je korak spojiti se preko njegove IP adrese koristeći **Putty**, jednostavno unese se SSH konekcija s IP adresom Raspberry Pi-ja pa kad zatraži unese se username i password. Nakon spajanja dobije se odmah shell:

![alt](/images/putty_bash.png)

Iz shella dalje treba pokrenuti konfiguraciju Raspberry Pi OS-a:
```sh
sudo raspi-config
```

Dobije se ekran Configuration Tool i preko njega obavezno postaviti autologin s userom **pi** (postavio defaultnog usera) radi kasnijeg automatskog pokretanja Python skripte projekta:

![alt](/images/raspi_config1.png)

Također obavezno treba omogućiti SSH server:

![alt](/images/raspi_config2.png)

Nakon izlaska iz raspi-config potrebno je postaviti statičku IP adresu kako ne bi morali svaki put tražiti koji je IP kad se Raspberry spoji na router. Za to se editira file **/etc/dhcpcd.conf**, od samih editora kroz shell koristim najviše **pico**:
```sh
pico /etc/dhcpcd.conf
```

U fileu je potrebno doći do ovog dijela u kojem se konfigurira statička IP adresa i inicijalno su sve linije u fileu zakomentirane s **#**. Linije kao u primjeru otkomentirati i izmijeniti prema adresi routera i željenoj fiksnoj IP adresi:
```sh
# Example static IP configuration:
interface eth0
static ip_address=<YOUR_RASPBERRY_IP>/24
#static ip6_address=fd51:42f8:caae:d92e::ff/64
static routers=<YOUR_ROUTER_IP>
static domain_name_servers=<YOUR_ROUTER_IP> 8.8.8.8
```
Pod **<YOUR_RASPBERRY_IP>** staviti željenu fiksnu adresu, može biti i ona pod kojom se prvi put automatski Raspberry spojio na router, a pod **<YOUR_ROUTER_IP>** staviti IP adresu routera, npr. neki automatski imaju 192.168.0.1 i ta adresa se ne mijenja. Promjene spremiti i izaći iz editora.

Nakon promjena restartati Raspberry:
```sh
sudo shutdown -r now
```

Za upload i download fileova (Python koda, GPX fileova) na Raspberryjevoj SD kartici dok je na mreži najbolje i najpraktičnije je koristiti FTP protokol i neki besplatni klijent kao što je npr. FileZilla. Zato kroz shell treba instalirati i FTP server:
```sh
sudo apt install vsftpd
```

Nakon instalacije slijedi konfiguracija FTP servera editiranjem filea **/etc/vsftpd.conf**:
```sh
sudo pico /etc/vsftpd.conf
```

U fileu kada se pronađu ove zakomentirane linije treba ih otkomentirati brisanjem **#**
```sh
#write_enable=YES
#local_umask=022
#anon_upload_enable=YES
```

Na kraj filea dodati sljedeće linije:
```sh
user_sub_token=$USER
local_root=/home/$USER/FTP
```

Spremiti promjene, izaći iz editora te kroz shell kreirati FTP share direktorij **FTP/share** u home direktoriju usera i dodati sva prava userima:
```sh
mkdir -p /home/pi/FTP/share
chmod 777 /home/pi/FTP/share
```

Restartai FTP deamon:
```sh
sudo service vsftpd restart
```

Ako je sve uspješno odrađeno može se spojiti na Raspberry preko nekog FTP klijenta.


## Raspberry Pi uparivanje i spajanje Bluetooth GPS modula

Nakon inicijalne konfiguracije slijedi provjera i uparivanje GPS modula s Raspberry Pi te je ovaj korak jako bitan za dalje. Inače po bootu Raspberryja pokreće se i Bluetooth servis pa se status servisa može provjeriti preko shell naredbe:
```sh
systemctl status bluetooth
```

Očekivan je rezultat aktivan Bluetooth servis kao u ovom primjeru:
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

Nakon što smo provjerili i potvrdili kako je servis aktivan potrebno je pokrenuti skeniranje Bluetooth uređaja u blizini. Naravno prije toga mora se upaliti vanjski Bluetooth GPS uređaj. Pronalaženje uređaja u blizini kroz shell:
```sh
hcitool scan
```

Rezultat skeniranja trebao bi biti lista Bluetooth uređaja s njihovim adresama i nazivima koji su vidljivi, npr.:
```sh
pi@raspberrypi:~ $ hcitool scan
Scanning ...
        00:02:78:19:70:30       HI-406BT
        4C:31:2D:73:88:88       MiTV-AYFR0
```

Korištenje **hcitool** je zapravo opcionalno (dobro posluži za kontrolu) pošto ću u nastavku za skeniranje i uparivanje koristit interaktivni tool **bluetoothctl** koji se pokreće kroz shell:
```sh
bluetoothctl
```

Nakon pokretanja pojavit će se njegov interaktivni shell kroz koji se upravlja uređajima:
```sh
Agent registered
[CHG] Controller B8:27:EB:F6:C0:3F Pairable: yes
[bluetooth]#
```

Prvo "upaliti" Bluetooth na samom toolu:
```sh
[bluetooth]# power on
Changing power on succeeded
```

Registrirati njegovog agenta:
```sh
[bluetooth]# agent on
Agent is already registered
```

Prebaciti na default agenta:
```sh
[bluetooth]# default-agent
Default agent request successful
```

Gornji koraci bili su "fire and forget" jer se samo oslanjam na metode koje provjereno rade. Nakon toga slijedi skeniranje okolnih uređaja i praćenje koji se pojavljuju kao rezultat (počet će se pojavljivati oni koji su vidljivi i kroz prethodno korištenje **hcitool**):
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

Iz gornjeg rezultata što vrati tool potrebno je pronaći adresu Bluetooth GPS modula prema njegovom imenu i dobro je zapamtiti pošto će se koristiti više puta kroz tutorial. Ključno je detektirati koji GPS modul koristite pošto se svaki drugačije predstavlja. U mom primjeru iz korištenih komponenti koje koristim pronašao sam adresu 00:02:78:19:70:30 koja odgovara imenu HI-406BT. Tako i u vašem slučaju pronađite koja adresa odgovara te uparite s naredbom **pair** iza koje slijedi adresa, ovo je moj primjer:
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

Odmah po pokušaju uparivanja kao što je gore vidljivo tražit će vas unos **PIN** koda za uparivanje, moj primjer i puno njih po defaultu imaju **0000**. Ako je sve prošlo uspješno vidjet ćete poruku **Pairing successful**. Prilikom uparivanja moguće je dobiti i ovakav tip greške:
```sh
[bluetooth]# pair 00:02:78:19:70:30
Attempting to pair with 00:02:78:19:70:30
Failed to pair: org.bluez.Error.AlreadyExists
```

> :warning: U tom slučaju najčešće je problem što je uređaj već na nešto povezan i u korištenju pa ga potrebno odspojiti iz konekcije s tim nekim drugim uređajem. Nakon toga ponoviti gornje korake. Ako ni to ne pomogne, može pomoći restart Bluetooth servisa.

Ako je do sada prošlo sve ispravno moguće je dobiti info o uređaju i statusu prema njegovoj adresi:
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

Nadalje, mogu se vidjeti svi upareni uređaji, najvažnije vidjeti GPS modul koji će se koristiti u projektu:
```sh
[bluetooth]# paired-devices
Device 00:02:78:19:70:30 HI-406BT
```

Na kraju pošto je sve prošlo ok treba izaći iz **bluetoothctl** toola jer više neće biti potreban:
```sh
[bluetooth]# exit
```

Idući korak je tool **rfcomm** koji se također koristi u Bluetooth konfiguraciji kroz shell:
```sh
rfcomm
```

Rezultat će biti adresa i status **RFCOMM** kanala na koji je spojen Bluetooth uređaj kao što je moj primjer:
```sh
rfcomm1: 00:02:78:19:70:30 channel 1 closed
```

Bitno je zapamtiti iz rezultata **rfcomm1** pošto će se koristiti u nastavku kao dio naredbe. Za spajanje na uređaj kroz shell potrebno je onda kombinirati **/dev/rfcomm1** i adresu uređaja iz prethodnih koraka:
```sh
rfcomm bind /dev/rfcomm1 00:02:78:19:70:30
```

> :warning:  Ako nemate prava pojavit će se sljedeća greška:

**Can't create device: Operation not permitted**

Rješenje je koristiti **sudo** za sam poziv naredbe:
```sh
sudo rfcomm bind /dev/rfcomm1 00:02:78:19:70:30
```

Ako smo do sada sve u ovim koracima dobro proveli, što znači već smo uređaj uparili i koristimo ga dobit ćemo sljedeću poruku koja je zapravo ok:
**Can't create device: Address already in use**

Izgleda kao upozorenje ili greška, ali je rezultat prethodnih alata koji su se koristili. Kasnije u nastavku ovakvo bindanje kroz **rfcomm1** će se iskoristiti u Python skripti.


## Python komunikacija s Bluetooth GPS modulom

Sada je na redu pisanje prvog Python programa za komunikaciju s Bluetooth GPS modulom. Minimalna verzija Pythona trebala bi biti 3.5, u mom slučaju je korištena 3.9.2, ali uvijek je dobro koristiti što višu verziju. Pošto je komunikacija preko Bluetootha serijska, prvo kroz shell provjeriti postoji li instaliran Python library **pyserial** koji će se koristiti pa je provjera:
```sh
pip3 list | grep pyserial
```

Ako gornja provjera ne vrati postojanje libraryja, potrebno ga je instalirati (ako javi grešku kako nema prava prebaciti se na **pi** usera sa **su pi**):
```sh
pip3 install pyserial
```

Vrijeme je za kreiranje novog Python filea **raspi-gps.py** koji će čitati serijsku komunikaciju i ispisivati što smisleno dobije. Serijska komunikacija čita preko porta koji se nalazi na deviceu **/dev/rfcomm1** što odgovara prethodnom poglavlju. Bitno je naglasiti kako će se taj port koristiti u nastavku, a također su bitni odrađeni koraci samog spajanja na Bluetooth iz prethodnog poglavlja. Za ovu prvu skriptu obavezno je prvo se spojiti na GPS modul prije pokretanja (pogledati prethodno korištenje **rfcomm bind**). U beskonačnoj petlji se pokušava pročitati znak na serijskom portu sve dok se ne dođe do **'\r'** kao kraj poruke i takva se ispiše. Source kod prve iteracije spajanja na GPS modul i serijske komunikacije:
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

Nakon malo proučavanja source koda pokrenuti ga kroz shell:
```sh
python3 raspi-gps.py
```

Ako je sve prošlo u redu od prethodnih koraka i kod pokretanja Python skripte nije bilo grešaka, trebale bi se uskoro pojavljivati kriptične linije slične kao što su u mom primjeru:
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

Ovo izgleda potpuno ispravno i radi se o **NMEA** podacima koji dolaze iz komunikacije s GPS modulom. U nastavku ćemo se pozabavit njihovim dešifriranjem.

Ukoliko se kod pokretanja pojavila neka greška u bindanju GPS modula i vidljivo je kao ispad Pythona znači samo kako je potrebno prije pokretanja iz shella ponovno pokrenuti bindanje. Kao i u prethodnim koracima pokrenuti **rfcomm bind** s adresom uređaja (dalje ću umjesto adrese koristiti **<YOUR_BLUETOOTH_MAC_ADDRESS>**) i provjerite status:
```sh
sudo rfcomm bind /dev/rfcomm1 <YOUR_BLUETOOTH_MAC_ADDRESS>
rfcomm
```

Kako korak bindanja ne bi morali ponavljati prilikom svakog pokretanja Raspberry Pi-ja i provjeravali status prije pokretanja Python skripte, dodao sam poziv bindanja odmah u skriptu. Time će se izvršiti kao poziv OS naredbe prilikom svakog pokretanja ove skripte:
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

Ponovno pokrenuti kroz shell:
```sh
python3 raspi-gps.py
```

Rezultat bi trebao biti isti, pojavljivat će se **NMEA** podaci GPS modula i manje treba voditi brigu o spajanju na modul, dovoljno ga upaliti i već nakon toga može se pokrenuti Python skripta koja će se njim početi komunicirati.


## GPS kodovi

**NMEA** (National Marine Electronics Association) je po imenu udruženje, a ovdje je bitna **NMEA-0183** specifikacija za komunikaciju prvenstveno namijenjena nautičkoj elektronici. Od toga najvažnije je što se koristi kao standard komunikacije GPS uređaja. Eksterni GPS uređaji preuzimaju signal s vidljivih satelita i uobličavaju ga u NMEA podatke koje dalje šalju kao u našem slučaju putem Bluetooth serijske komunikacije. Sami podaci koji se šalju sadrže identifikator trackera (GPS, Galileo, GLONASS, BeiDou), skupinu poruke koja se šalje i podatke koji odgovaraju skupini. Detalji sa skupinama i sadržaju poruka može se vidjeti na linku [NMEA Sentences](https://receiverhelp.trimble.com/alloy-gnss/en-us/NMEA-0183messages_MessageOverview.html).

Svaka poruka koja se zaprimi (NMEA sentence) počinje s **$** i oznakom trackera pa tako iz gornjeg primjera dolazi **$GP** što je oznaka za **GPS**. Ako vaš modul podržava i ostale sustave mogli bi dobiti početak poruke s npr. $GA za Galileo. Dalje se orijentiram na GPS pa dekodiram poruke koje počinju s **$GP**. Nakon oznake trackera dolazi skupina kojoj pripada poruka i za projekt, a i inače najvažnije su mi **GGA - Global Positioning System Fix Data** i **VTG - Track made good and Ground speed**.  GGA u podacima sadrži meni bitne: zemljopisnu širinu, dužinu, visinu i orijentaciju, ostale neću koristiti. VTG mi je zanimljiv samo radi očitanja brzine, ostale ne koristim.

Potrebne podatke sam ekstrahirao prema grupi i poziciji unutar poruke, za što mi je pomogla dokumentacija NMEA poruka, a dalje je stvar prezentacije podataka. Ovdje je izazov što je vrijednost pozicije zemljopisne širine i dužine malo drugačija od očekivanja pa je potrebno pretvoriti iz NMEA formatiranog podatka (format je (d)ddmm.mmmm gdje je **d** stupanj, a **m** minuta) u decimalni. Tu mi je za potvrdu konverzije morao malo pomoći jedan članak na [Stack Overflow](https://stackoverflow.com/questions/36254363/how-to-convert-latitude-and-longitude-of-nmea-format-data-to-decimal) pa sam u Pythonu kreirao i funkciju za konverziju.

Gornji Python program sam prema tome nadogradio. Pročitanu poruku s GPS, odnosno NMEA kodovima ekstraktam i provjeravam sadrži li potrebne grupe GGA i VTG te iz njih uzimam potrebne vrijednosti. Za prikaz pozicije dodatno konvertiram vrijednost u stupnjeve i dodajem pročitanu orijentaciju. Sada tako nadograđen i uljepšan Python kod izgleda ovako:
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

Ponovno pokrenuti kroz shell:
```sh
python3 raspi-gps.py
```

Rezultat bi trebao biti formatiran ispis trenutne pročitane GPS pozicije, visine i brzine ako se ona uspješno pročita i mijenja.


## Kreiranje GPX filea

Nakon pokretanja i testiranja ovog programa slijedi zapisivanje GPS pozicija u file, konkretno koristit ćemo **GPX** format. **GPX** ([GPS Exchange Format](https://en.wikipedia.org/wiki/GPS_Exchange_Format)) je XML schema za zapis GPS podataka radi korištenja u drugim aplikacijama, a u ovom tutorialu koristit ćemo ga za zapisivanje staze (track). Tako rezultira tracking našeg Raspberry Pi uređaja. Pri pokretanju će se uvijek kreirati novi jedinstveni **.gpx** file u koji će se ukoliko se promijeni pozicija nakon 10 sekundi zapisivati nova točka staze. Razlog zapisivanja samo promjene lokacije i to ako se događa nakon 10 sekundi je smanjenje samog filea, nema potrebe istu poziciju zapisivati u file ili baš svaku najmanju promjenu. Tim parametrima se može manipulirati, samo malo treba modificirati skriptu.

Za kreiranje **GPX** formata u Pythonu koristit ćemo library **gpxpy** - [GPX File Parser](https://pypi.org/project/gpxpy/). Prvo je potrebna provjera instalacije libraryja:
```sh
pip3 list | grep gpxpy
```

Ako gornja provjera ne vrati postojanje libraryja (inicijalno nije instaliran), potrebno ga je instalirati (ako javi grešku kako nema prava prebaciti se na **pi** usera sa **su pi**):
```sh
pip3 install gpxpy
```

Korištenje libraryja sastoji se od kreiranja objekta i pripadnih staza (trackova) i segmenata koji sadrže točke. Točke su pojedina GPS pozicija koju ćemo zapisati u objekt koji rezultira spremanjem u GPX file. Pošto se pozicija u GPX objektu ne može zapisati točno kako smo je pročitali iz komunikacije, odnosno NMEA poruke, potrebno ju je malo prilagoditi. Jedan oblik prilagodbe je sam format ispisa što sam napravio u prethodnoj Python skripti pa ću to iskoristiti, a dalje slijedi još jedan dodatak. Naime, orijentacija pozicije (N, S, E, W) je samostalna u NMEA poruci, ali je u GPX formatu sadržana u zemljopisnoj širini i dužini. Zbog toga orijentacije S i W množim s -1 kako bi ih pretvorio u GPX format. Također bitna stvar u zapisivanju je i točno vrijeme koje mora biti u **ISO 8601** formatu.

U doljnjem kodu može se vidjeti kako skripta ne zapisuje brzinu u GPX objekt. Razlog tome je što se po defaultu koristi GPX verzija 1.1 koja ne sadržava brzinu. Ukoliko se želi zapisati i brzina (za auto entuzijaste), potrebno je koristiti verziju GPX 1.0. To bi bila manja prilagodba u tome što se brzina treba dodati na kraj parametara poziva ```gpxpy.gpx.GPXTrackPoint``` kao ```speed = speed``` i poziv ```gpx.to_xml()``` zamijeniti s ```gpx.to_xml(version="1.0")``` dok ostalo ostaje isto. Nekome može biti dodatan izazov i što se brzina čita iz VTG poruke, a ostalo iz GGA poruke prema kojoj se trenutno i zapisuje.

Dodatna sitna fukcionalnost koju sam ugradio nalazi se na početku izvršavanja Python skripte, a odnosi se na čitanje argumenata s kojima smo je pozvali. Dobro može doći kod pripreme uparivanja i početka komunikacije s GPS modulom. Naime, ako se kao argument proslijedi neki broj, skripta će pauzirati toliko sekundi prije nego nastavi dalje s radom. Ova funkcionalnost će se iskoristiti u idućem poglavlju.

Nova iteracija Python koda nakon dodavanja opisanih funkcionalnosti sada izgleda ovako:
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

Pokrenuti kroz shell:
```sh
python3 raspi-gps.py
```

Rezultat što se tiče samog ispisa trebao bi biti isti kao u prethodnom Python kodu, ali će se u istom folderu također kreirati **.gpx** file koji će se povećavati kako se bilježe promjene GPS pozicije.


## Automatsko pokretanje Python skripte

Sada je Python skripta već dovoljno kompletirana pa bi se mogla automatski pokretati svaki put nakon što se boota Raspberry Pi umjesto kao do sada ručnim pokretanjem. Ručno pokretanje je u redu kada se ovako doma programira i testira, ali finalno kada je u živom radu pokretanje mora biti automatsko i to što prije. Kako bi se dodalo automatsko pokretanje prilikom bootanja potrebno je editiranje filea **/etc/rc.local**, opet koristim pico: 
```sh
sudo pico /etc/rc.local
```

Potrebno se pozicionirati prije linije **exit 0** i dodati sljedeće linije:
```sh
cd /home/pi/FTP/share
sudo -u pi python3 raspi-gps.py 30 > log.txt 2>&1 &
```

U mom slučaju file izgleda ovako:

![alt](/images/putty_rc_local.png)

Ovom promjenom prvo se u izvođenju pozicioniramo u direktorij gdje se nalazi Python skripta. Nakon toga se pod userom **pi** (ovo je obavezno) pokreće Python skripta **raspi-gps.py** s parametrom čekanja od 30 sekundi (što bi trebalo biti dovoljno za podizanje svih servisa o kojima zavisi), output pokretanja skripte prosljeđuje se u log file **log.txt** kako bi se u njemu mogle vidjeti greške pokretanja, a na kraju cijelog reda obavezan je znak **&** kojim se tako pokrenut proces izvršava u backgroundu.

Parametar u pokretanju koji se odnosi na čekanje od 30 sekundi sam spomenuo u prethodnom poglavlju i odnosi se na ovaj dio koda Python skripte pa ako se se proslijedi neki drugi broj toliko će sekundi čekati na nastavak izvršavanja:
```python
# from argument set sleep
if len(sys.argv) > 1:
  time.sleep(int(sys.argv[1]))
```

Nakon spremanja promjene filea **/etc/rc.local** potrebno je restartati Raspberry Pi kroz shell:
```sh
sudo shutdown -r now
```
ili
```sh
sudo reboot
```

Time će se ako je sve prošlo ispravno automatski pokrenuti Python skripta. Ako je došlo do greške, ona je vidljiva u istom folderu u fileu **log.txt**.

Bitno je spomenuti i ako se nakon uspješnog pokretanja ponovno spajamo Puttyjem na Raspberry Pi te mijenjamo skriptu potrebno je prije ručnog pokretanja nove verzije kill-ati postojeći proces. Provjera pokrenute skripte kroz shell:
```sh
ps -fu pi | grep raspi-gps
```

Prema rezultatu pronaći ```<pid>``` aktivnog procesa te kroz shell pozvati ```kill <pid>``` tog procesa.


## Korištenje gumba i RGB LED-ice

Do sada je izrađena osnova GPS trackera koji se u ovom obliku može i sam koristiti, ali tada nema interakcije. Vrijeme je za upogoniti gumb koji je u ovom projektu jedini oblik interakcije zajedno s RGB LED signalizacijom rada Raspberry Pi-ja. U tu svrhu kreirat ćemo novi Python file **gpio_test.py** radi isprobavanja spojenog gumba i paljenja / gašenja RGB LED-ice u različitim bojama.

Način spajanja gumba i RGB LED-ice s Raspberry Pi-jem vidjeli smo još na početku u poglavlju [Komponente](#komponente). Komponente su spojene na Raspberry Pi pinove napona, uzemljenja i one koji se mogu koristiti za opću namjenu. Raspored pinova i koje su im namjene može se vidjeti na linku [Raspberry Pi Pinout](https://pinout.xyz/) ili kroz shell:
```sh
pinout
```

Izabrao sam pinove koji mi odgovaraju prema smještaju, u vlastitoj verziji projekta možete koristiti i neke druge uz izmjene u kodu. U narednoj skripti za testiranje koristit ću pin **GPIO3** za očitanje pritiska gumba, **GPIO17** za crveni pin, **GPIO22** za zeleni pin i **GPIO10** za plavi pin RGB LED-ice. Dodatno ću iskoristiti pin **GPIO27** kao naponski pin.

Za upravljanje GPIO pinovima koristit će se **gpiozero** interface koji bi već trebao biti instaliran u sklopu Pythona na Raspberry OS-u. Koriste se njegove klase Button, LED i RGBLED te svakoj od njih dodjeljuje rad s pojedinim pinom. Programiranje je relativno jednostavno i intuitivno, sastoji se od paljenja / gašenja pojedinih pinova ili očitanja stanja gumba na pinu. Source kod **gpio_test.py** za upravljanje gumbom i RGB LED-icom tako izgleda ovako:
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

Nakon malo proučavanja source koda treba ga pokrenuti kroz shell:
```sh
python3 gpio_test.py
```

U inicijalizaciji se prvo dodjeljuju svakoj klasi pojedini pinovi. Odmah se na dvije sekunde RGB LED-ica treba upaliti crveno, zeleno pa plavo. Način korištenja klase RGBLED, odnosno puštanje napona na pojedini pin koji upravlja bojom kako je vidljivo u sourceu ovisi o korištenoj RGB LED-ici, a u mom primjeru koristim onu sa zajedničkom anodom (+). Nakon paljenja pojedine boje program provjerava stanje gumba, ako je pritisnut dulje od 5 sekundi RGB LED-ica će zasvijetlit crveno, kraće od toga će zasvijetlit žuto, a ako gumb nije pritisnut zasvijetlit će zeleno. I nakon jedne sekunde ide iduća iteracija petlje. Za svaki slučaj u testu statusi pritisnutog gumba i koja boja se pali se ispisuju prilikom izvođenja.


## Kompletiranje Python koda

U ovom poglavlju se dosadašnje Python skripte objedinjuju u finalni Python kod projekta koji će upravljati Bluetoothom, GPS modulom, gumbom i RGB LED-icom.

Osim toga iskoristit ću priliku neke postojeće funkcionalnosti izdvojiti u klase i dodati nove funkcije. Tako sam kreirao novu klasu **Color** kao enumeracija za paljenje pojedinih boja na RGB LED-ici. Kreiranje i zapisivanje rute izdvojio sam u novu klasu **Recorder**. Za ispade programa dodatno imam funkciju **terminate** i za gašenje Raspberry Pi-ja funkciju **shutdown**. Od novog većeg seta linija koda dodao sam detekciju pritiska gumba i ovisno o duljini pritiska mijenjaju se statusi početka ili kraja snimanja rute zajedno sa signalizacijom LED-icom te sam još dodao novu fukcionalnost gašenja cijelog Raspberry Pi-ja. Ispod source koda nalaze se i kraće upute.

Finalni ovako kompletiran **raspi-gps.py** sada izgleda ovako:
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

Nakon malo proučavanja source koda treba ga pokrenuti kroz shell, ali sada zbog kompleksnosti dobro je kao novi korak prvo provjeriti sintaksu skripte:
```sh
python3 -m py_compile raspi-gps.py
python3 raspi-gps.py
```

Sada će program počet signalizirati svoj rad.

RGB LED-ica signalizira plavom bojom korak spajanja na GPS modul. Ako se tokom tog procesa dogodila neka pogreška zasvijetlit će crveno na 2 sekunde i program prestaje s radom. U tom slučaju nema druge nego pogledati u **FTP/share** folderu log s greškom. Takve greške su trebale biti vidljive i ranije tokom testa. Inače ako je sve dobro prošlo po prethodnim koracima i zamijenjeno što je označeno u Python skripti prema tutorialu ne bi trebalo biti problema.

Kada je uspješno uparen GPS modul s Raspberryjem program povremeno odaje neke dodatne signale o radu. Prilikom snimanja rute ako se promijeni pozicija svakih 10 sekundi zasvijetlit će zeleno. Ako se nije skroz pozicionirao prema satelitima i ne očitava točno poziciju blinkat će crveno. Pritiskom gumba dok se ne snima ruta LED-ica će zasvijetlit zeleno. Dovoljno držati gumb 0,5 sekunde kako bi se pokrenulo snimanje rute. Suprotno, dok program snima rutu pritiskom gumba LED-ica će zasvijetliti crveno. Držanjem tako gumba 0,5 sekundi prestat će se snimati ruta. Zato je isti gumb u modu on/off pa će za pokretanje zasvijetliti LED-ica zeleno, a zaustavljanje crveno.

Svako snimanje kreira poseban **.gpx** file u folderu **FTP/share** koji se može downloadati i dalje otvoriti u nekom samostalnom softwareu kao što je npr. Google Earth radi vizualnog pregleda rute. Za sam kraj rada Python programa, ali i gašenje cijelog Raspberryja potrebno je držati pritisnut gumb 10 sekundi što će isto signalizirati crvenom LED-icom. Kada se želi ponovno pokrenuti, ponoviti cijeli gornji ciklus, odnosno fizički upaliti Raspberry.

I to su upute za korištenje. :smiley:


## Projekt u živom radu

Nakon testa cijelog sustava doma na stolu i PC-u vrijeme je za pravo korištenje u realnim uvjetima, u mom slučaju vožnji jednom rutom. Spajanjem Raspberryja na USB auta ili powerbank počinje se bootati i nakon toga odmah pokreće Python skriptu. Znači kad se boota Raspberry odmah upaliti i eksterni GPS modul kako bi se upario Bluetoothom te što prije pozicionirao prema vidljivim satelitima. Dalje je stvar trenutka kada palite i gasite snimanje rute putem gumba prema uputama iz prethodnog poglavlja.

Jedna moja tako snimljena ruta je u primjeru:

[![Download Icon]][def-gpx-sample]

**.gpx** file sam otvorio u Google Earthu i slika je u nastavku. Inače je alat dovoljno intuitivan pa nakon učitavanja rute i njenog iscrtavanja prikazat će dodatne gumbe na svom sučelju.

[![](/images/Google_Earth_gpx_small.png)](/images/Google_Earth_gpx.png)


## Off topic pojednostavljenje s manje komponenti

Ako se koristi kao u mom slučaju Raspberry Pi Zero W i sam projekt se želi još više pojednostavniti smanjenjem broja komponenti, mogla bi se iskoristiti interna LED-ica Raspberryja umjesto RGB LED-ice na eksperimentalnoj pločici. Korak dalje, ako se ne bi koristili otpornici i raducirao broj žica došli bi do samo spajanja gumba na Raspberry kao na ovom minimalnom dijagramu:

![alt text](/images/Raspberry_Pi_Bluetooth_GPS_simple.png "Fritzing dijagram - Raspberry Pi Zero W s minimumom komponenti")

Izgleda asketski i izuzetno kompaktno, a paljenje i gašenje interne LED-ice moguće je s malo hacka pošto će se pozivati shell naredbe. Radi se o zapisivanju high (1) ili low (0) vrijednosti u datoteku **/sys/class/leds/mmc0/brightness** što nije izvedivo preko običnog usera pa ćemo koristiti **sudo**.

Paljenje interne LED-ice kroz shell:
```sh
sudo sh -c "echo 1 > /sys/class/leds/mmc0/brightness"
```
Gašenje interne LED-ice kroz shell:
```sh
sudo sh -c "echo 0 > /sys/class/leds/mmc0/brightness"
```
Ako ne uspije od prve samo treba ponovno pokrenuti naredbe kroz shell.

Kako upaliti i ugasiti internu LED-icu putem gumba, a isprogramirano kroz jednostavnu Python skriptu? U nastavku je implementacija koja poziva shell naredbe iz Pythona, prvo se isprobavaju pozivi spremanja high i low vrijednosti te nakon toga se prati pritisak gumba na pinu GPIO3. Držanjem gumba 5 sekundi upali se LED-ica, svijetli sekundu i nakon toga se ugasi.

Kreirati file **internal_led_test.py** sa source kodom:
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

Pokretanje Python skripte kroz shell:
```sh
python3 internal_led_test.py
```

Ako je sve ok, uz malo intervencije relativno lako možete samostalno doraditi **raspi-gps.py** kako bi Raspberry radio s internom LED-icom. :yum:


## Reference

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
