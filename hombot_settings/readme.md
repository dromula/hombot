# Config of Hombot

The Hombot is controlled via the WLAN. To enable the connection via the Internet, the robot connects to the VPN of my Fritzbox.  The settings that were made in the progress of the project are listed here.

## VPN Config

### Logfile erstellen
The logs should all be written to one file. For this first a log file is created.

```
touch /home/pi/log.txt
```

### Fritzbox VPN configuration
Add contents of fritzbox.conf and replace your settings and credentials to /etc/vpnc/fritzbox.conf
```
sudo nano /etc/vpnc/fritzbox.conf
```

### Start VPN after boot
Firstly the VPN has to be started. To do this, add following lines *before* ```exit 0```:
```
sleep 15
sudo vpnc fritzbox.conf > /home/pi/log.txt 2>&1
```

### Script to keep VPN connection
Sometimes connection to the Fritzbox gets lost. Write contents of ```autovpnscript.sh``` to ```/etc/init.d/autovpnscript.sh ```

We use an cronjob to start the autovpnscript and check the connection every minute. 
Add this to /etc/crontab 
```
* * * * * root sh /etc/init.d/autovpnscript.sh >/dev/null 2>&1
```

## WLAN Configuration (optional)

Because I also want the Hombot to be functional outside the house, it should primarily use the access point of my smartphone as a WLAN connection. However, for testing purposes, I have also configured my home WLAN. The individual connections are prioritized, the access point gets the higher prioritization. To use my configuration, copy the contents of the ```wpa_supplicant.conf``` into the file ```/etc/wpa_supplicant/wpa_supplicant.conf``` and replace it with your credentials.
```
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
```
