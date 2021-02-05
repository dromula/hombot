#!/bin/bash

# set -x auskommentieren für den Debug Modus. Die Ausgabe erscheint in der Kommandozeile.

#set -x

# hier wird die Logfile-Datei definiert
# Logfile muss erst mit „sudo nano fritzbox.log“ am Zielort erstellt werden erstellt werden

LOGFILE=/home/pi/log.txt

# hier wird die IP-Adresse von Fritzbox definiert. wenn die VPN Verbindung steht, dann sollte ping funktionieren.

myHost=192.168.178.1

# Wert -> wie oft soll gepingt werden

wert=4

# Ausgabe Wert für „count“ soll bei erfolgreichen ping 4 sein, bei erfolglosen ping 0.

count=$(ping -I tun0 -c $wert $myHost | grep 'received' | awk '{print $4 }')

echo "Count $count:$wert:$myHost"

if [ $count -gt 2 ]; then

        # die kommenden echos sind die Info-Ausgaben in Logfile
        echo "$(date +%Y-%m-%d:%T) :Fritzbox mit der IP $myHost ist erreichbar und VPN Verbindung steht. Count $count" | tee -a $LOGFILE

else

        echo "" | tee -a $LOGFILE
        echo "$(date +%Y-%m-%d:%T) :Fritzbox mit der IP $myHost ist nicht erreichbar. Count: $count" |tee -a $LOGFILE
        echo "$(date +%Y-%m-%d:%T) :VPN-Verbindung trennen" |tee -a $LOGFILE

        #hier wird das VPNC-Demon gestoppt, damit es nicht meher im Hintergrund lauft
        /usr/sbin/vpnc-disconnect

        # oft ist die Wlan Verbindungen unterbrochen. hier werden alle Netzwerkverbindungen neugestartet.

        echo "$(date +%Y-%m-%d:%T) :Netzwerkverbindungen neu starten" | tee -a $LOGFILE

        /etc/init.d/networking restart

        # 12 Sekunden warten

        sleep 12

        # auslesen von der Wlan Ip-Adresse
        # grep Adresse muss bei Englischen Spracheinstellungen evtl. geändert werden. Mit dem Debug Modus ausprobieren

        ipwlan=$(/sbin/ifconfig wlan0 | grep „inet Adresse“ | cut -b 24-38)

        echo "$(date +%Y-%m-%d:%T) :Netzwerkverbindungen wurde neugestart. WLAN IP-Adresse: $ipwlan " | tee -a $LOGFILE

        echo "$(date +%Y-%m-%d:%T) :VPN Verbindung neu aufbauen, der Skript vpnc_fritzbox starten" | tee -a $LOGFILE

        # starten von VPNC-Demon. PID und VPN-IP Adresse auslesen

        /usr/sbin/vpnc fritzbox.conf

        pid=$(pidof vpnc)

        ipvpn=$(/sbin/ifconfig tun0 | grep „inet Adresse“ | cut -b 24-38)

        echo "$(date +%Y-%m-%d:%T) :Die VPN-Verbindung wurde erfolgreich aufgebaut. die VPN IP-Adresse ist: $ipvpn. VPNC-Demon ist aktiv unter id: $(pidof vpnc)" | tee -a $LOGFILE

        echo "" | tee -a $LOGFILE

fi

