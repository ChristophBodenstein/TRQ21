### Vorwort
Ich schreibe dies auf deutsch, da die meisten Leute, die es interessiert, vermutlich aus Deutschland sind. Ich bin mir nicht sicher, ob diese Art der Heizung in anderen Ländern gebräuchlich ist. Falls doch, schreibt mir und ich werde das bei Gelegenheit übersetzen.

I´m writing in german because most people interested in this probably are german. Maybe this type of heating isn´t used at all outside of Germany. If I´m wrong and this is needed in englisch, please leave a comment or just use google translate ;-)


# Motivation
Viele Wohnungen werden mit sogenannten Gas-Etagen-Heizungen beheizt. Im Gegensatz zur Zentralheizung, wird dafür nur eine Gasleitung bis in die Wohnung verlegt. Dort erhitzt eine Gastherme das Heizungswasser und pumpt es durch die Heizkörper der Wohnung.
Das hat viele Vorteile, für den Vermieter:

* Es ist keine Abrechnung der Heizkosten notwendig.
* Es ist billiger, als Heizungsrohre durch das ganze Mietshaus zu verlegen.
* Jeder Mieter ist selbst verantwortlich, die schlechte Dämmung des Hauses fällt nicht so leicht auf.

Um die Gastherme ein- oder auszuschalten, also warmes Heizungswasser anzufordern, wird i.d.R. genau ein Raum-Temperatur-Regler verbaut. Üblicherweise in dem Zimmer mit dem höchsten Wärmebedarf. Das ist oft das Wohnzimmer.

Und genau da liegt das Problem. Die Temperatur in diesem Raum (und die Einstellung der Zieltemperatur am Fühler) gibt vor, ob die Gastherme Wärme produziert oder nicht. Alle Heizköper in allen Zimmern sind davon abhängig und regeln (sofern die Gastherme läuft) lediglich mit ihren Thermostaten herunter.

Je mehr Zimmer und Heizkörper eine Wohnung hat, desto schwieriger wird es, jedes Zimmer auf "seine" Zieltemperatur zu bringen und nicht darüber hinaus.
Richtig absurd wird es, wenn die Heizung eines mehrstöckigen Hauses mit nur einem Temperaturfühler gesteuert wird.

Die Folge ist entweder, dass einzelne Zimmer nicht warm genug, oder große Mengen Energie(Gas) verschwendet werden.

Ziel der ganzen Übung hier ist, jedes Zimmer einzeln auf eine eingestellte Temperatur zu bringen. So können nicht benötigte Zimmer gezielt unbeheizt bleiben. Auch das Zimmer mit dem Raum-Temperatur-Regler. In meiner bisherigen Erfahrung sinkt der Gasverbrauch dadurch um ca. 30% ohne Verlust an Komfort. Das hängt aber stark von der Wohnung und dem Nutzungsprofil ab. Für Ein-Raum-Wohnungen ist das ganze völlig nutzlos.

# Lösungsidee
Die Lösung liegt auf der Hand und viele Menschen haben dazu schon Anleitungen veröffentlicht. 

### In Kürze

* Alle Temperaturen an allen Heizkörpern müssen bekannt sein (Soll- & Ist-Temperatur)
    * Das kann man über Homematic (mit CCU3) oder Zigbee-Thermostate erledigen
* Bestimmen, ob die Heizung laufen soll, also ein Heizkörper unter seiner Zieltemperatur ist
* Den Raum-Temperatur-Regler übersteuern. --> __Das ist das zentrale Thema hier.__


### Etwas ausfühlicher
Ich verwende einen Raspberry Pi 4 mit Hm-IP-RFUSB-Stick. Auf dem Raspberry Pi läuft Homeassistant und darin die die simulierte Homematic CCU. Darüber kann ich alle Thermostate konfigurieren und vor allem auslesen.
Aus allen Soll- und Ist-Temperaturen "berechne" ich einen Gesamtwert für "Heizen". Abhängig von diesem Gesamtwert wird der Raum-Temperatur-Regler bzw. dessen Steuersignal überschrieben.
Als Raum-Temperatur-Regler ist bei mir ein Junkers TRQ-21 verbaut. Dieser ist mit 3 Kabeln angeschlossen. Die sog. Junkers 1-2-4-Schnittstelle.
* Ground
* 24V Versorgungsspannung
* Signalleitung mit 0..20V (Das Signal müssen wir erzeugen)

Zur Steuerung verwende ich einen ESP-Node, eingebunden mit ESPHome in Homeassistant, das geht angenehm unkompliziert.
Dies ist auch der zentrale Teil, der an jede Heizung angepasst werden muss. Wenn ihr einen anderen Raum-Temperatur-Regler habt, müsst ihr euch erst mal kundig machen, wie dieser seine Signale an die Gastherme übermittelt.
In meinem Fall ist es einfacher, als gedacht. Denn auch wenn der TRQ-21 eigentlich ein stetiges Signal zwischen 0 und 20 V liefert, geht meine Heizung bei über 9V an und unter 7V wieder aus. Also erzeuge ich einfach 12V oder 0V und fertig.
Hier nochmal die Liste der Bauteile, die grundsätzlich nötig sind, bevor es losgeht (das ist noch nicht die Bauteilliste für die Steuerplatine des ESP.)

* Raspberry PI4 + große SD-Card + Netzteil, gibt's. z.b. bei [BerryBase](https://www.berrybase.de/raspberry-pi-4-computer-modell-b-8gb-ram)
* [Hm-IP-RFUSB](https://de.elv.com/elv-homematic-ip-arr-bausatz-rf-usb-stick-fuer-alternative-steuerungsplattformen-hmip-rfusb-fuer-smart-home-hausautomation-152306)
* [ESP-Node](https://www.az-delivery.de/en/products/d1-mini)
* Homematic IP Thermostate (Die HM-IP-Basisstation nutze ich nicht)
    * Ich denke, dass ZigBee-Thermostate die bessere Wahl wären, hab ich aber nicht probiert. In dem Fall ist noch ein ZigBee-Gateway nötig, das gibt es auch bei BerryBase.


# Schaltung
## Originalschaltung
Die Originalschaltung habe ich auf Github gefunden:
https://github.com/RobinMeis/Junkers_1-2-4_ESP32
Großer Dank geht raus dafür. Mit dieser Schaltung lässt sich die Signalspannung von 0V..20V erzeugen. Allerdings musste ich ein paar Anpassungen vornehmen.
Ich hab die Schaltung mit Fritzing gemacht. Profis werden sicher eine andere Software nutzen. Hierfür hat's aber gereicht.
Wer die Platine bestellen möchte, kann das z.B. bei PCPWay tun. 5 Platinen kosten da ca. 15,- € inklusive Versand nach Deutschland. Die Gerberfiles hab ich deshalb mit abgelegt.

![TRQ-21-Replacement-Schaltung](Bilder/Schaltung_Leiterplatte.jpg?raw=true "Platine")

## Änderungen / Erweiterungen
### Pull-Down-Widerstand
Mein TRQ-21 liefert zwar im Testbetrieb, abhängig von der eingestellten Temperatur das korrekte Steuersignal. Jedoch liegt auf der Signalleitung (aus der Wand) auch ohne den TRQ-21 eine Spannung von 21V an. Das hatte ich nicht erwartet und gemäß Beschreibungen im Internet sollte das auch nicht so sein. Erst dachte ich, ich müsse statt Spannung zu treiben, hier nur Spannung herunterziehen. Deshalb hab ich die zwei Pull-Down-Widerstände vorgesehen. Einen, um grundsätzlich von 21V auf etwa 12V zu kommen und einen weiteren, den ich per Transistor ansteuere, um die Spannung unter 5V zu ziehen.
Ist aber nicht notwendig. R2 mit 2 kOhm zu bestücken reicht aus, um die Spannung weit genug herunter zu ziehen. Die Kurzschlussspannung der Signalleitung war bei mir nur 4 mA.
D.h. die restliche Schaltung bzgl. des OPV bleibt gleich.
R2: 2K Ohm
R1: Nicht notwendig

### Spannungsversorgung
Ich habe einen [LM2574](https://de.aliexpress.com/item/4000163896598.html) zur Spannungsversorgung vorgesehen. Der ist deutlich stromsparender und damit auch kühler, als Linearregler (LM7805) und relativ preiswert. Allerdings braucht man ein paar zusätzliche Teile auf der Platine.

### Nicht benötigte Teile
Einige Teile hab ich auf der Platine vorgesehen, weil es grade Spaß gemacht hat, für die grundsätzliche Funktion sind sie nicht notwendig.

* DHT Temperatur und Feuchtigkeit
* Pull-Down-Widerstand mit Transistor (R1 / Q1)
* Lüfteransteuerung (Q2, nicht getestet!)


### BOM
Die (hoffentlich vollständige Liste aller Teile auf der Platine)
* ESP-Node
* DHT11-Sensor (optional)
* Spannungswandler: LM2574*-5 (5V)
* OPV: LM358
* Spule: 330 µH
* Elko: 220µF
* Elko: 22 µF (Ich nutze hier 15µF, geht scheinbar auch)
* Transistoren (Q1/2): TIP121 hatte ich vorgesehen, dann aber DI1609 verbaut. Ist glaube egal, zumal sie eh nicht zwingend benötigt werden. Schaut einfach, dass sie pinkompatibel sind.
* Kondensator: 100 nF
* Widerstände:
    * 100 Ohm
    * 4,7 kOhm
    * 10 kOhm
    * 100 kOhm
    * 2 kOhm (R2)
* Dioden: Ich weiß ehrlich gesagt nicht, welchen Typ ich genau verbaut habe, einfach einen robusten Typ, den ich im Schrank hatte.
* Stiftleisten, wer das so machen möchte (Ich habe einfach Kabel mit Steckverbindern an die Platine gelötet.):
    * 3-polig für G/24V/Signal
    * 4-polig fürs Display (optional)
    * 2-polig für einen Lüfter (optional)
* Display: Ich hab ein [OLED-Display](https://www.az-delivery.de/products/0-96zolldisplay) verwendet, weil das sehr einfach zu integrieren war. Es wird per I2C angesteuert. Die Reset-Leitung des Displays wird nicht verwendet. D.h. zum ausprobieren muss man stets das ganze Ding ab/anschalten.


# Gehäuse
![FreeCad-Modell des Gehäuses](Bilder/Heizungsbox_offen.jpg?raw=true "Gehäusemodell")
## Anforderungen
An das Gehäuse hatte ich folgende Anforderungen:
* Platine sollte drauf passen
    * Schraubenlöcher sollten vorhanden sein
    * Platzierungsnasen sollten vorhanden sein, damit sie quasi einrastet beim Einbauen.
* Lüftungslöcher
    * Durch den Spannungswandler entsteht doch etwas Wärme, die sollte abziehen können.
    * Lüftungslöcher oben hab ich vergessen, ich empfehle das nachzuholen, notfalls mit einem Bohrer nach dem Drucken.
* Kabelloch
    * Zum Durchführen des Anschlusskabels.
* Displayöffnung
    * Damit das I2C-Display leicht montiert werden kann.
* Leicht zu öffnen (durch schieben nach oben)
    * Wegen Fehlersuche und so

Leider hab ich bei der Konstruktion 2 Fehler gemacht, die mehr oder weniger schwerwiegend sind. Einerseits hab ich die oberen Lüftungslöcher vergessen, was ich mit einem Bohrer schnell korrigiert habe. Andererseits ist die Platine "falsch herum" drin. Das Anschlusskabel sollte rechts unten sein, ist aber leider links oben. Ich hab einfach ein längeres Kabel verwendet, aber das Plan war eigentlich anders.
Außerdem sind die Gewindelöcher für die Displaybefestigung etwas zu flach geworden, aber notfalls kann man das auch mit Heißkleber befestigen.


Die STL-Dateien können direkt gedruckt werden. Alles was noch gebraucht wird, sind 4 Schrauben für das Gehäuse + 2 Schrauben zum Befestigen der Platine + 4 Schrauben für das Display.
Wer das Gehäuse ändern will kann:
* Die FreeCad-Datei öffnen und Änderungen machen.
* Die FreeCad-Datei öffnen und das Python-script ausführen bzw. vorher manipulieren.

Das Python-Script habe ich mit etwas Hilfe von ChatGPT erstellt. Es erzeugt die Einzelteile in FreeCad. Wer also besser Python kann, als FreeCad, der sollte damit glücklich werden.

![Kompletter Aufbau](Bilder/Kompletter_Aufbau.jpeg?raw=true "Eingebaute Infrastruktur")


# Einbinden in Homeassistant
Wie man Homeassistant und ESPHome einrichtet, kann an anderer Stelle nachgelesen werden. Hie geht's jetzt nur um die zwei wichtigsten Dinge auf der Platine.
Folgende Dinge finden sich anderswo im Netz und werden hier nicht weiter erläutert:

* Ansteuerung des Displays, fonts, Datenübertragung von HA nach ESPHome zur Anzeige von weiteren Infos
* Einbindung des DHT11
* Ansteuerung des (optionalen) Transistors für den zusätzlichen Pull-Down oder

### Einbinden der Spannungsmessung
Folgender Code-Schnipsel kommt in die YAML-Datei des ESPNodes.

```
sensor:
  - platform: adc
    pin: A0
    id: "HeatSignal"
    name: "Steuersignal der Heizung"
    update_interval: 10s
    filters:
      - multiply: 36.3
```

Den Faktor von 36.3 hab ich einfach durch Ausprobieren bestimmt. Den sollte man also nochmal prüfen.

### Einbinden des Ausgangs als Lichtschalter (PWM)
Folgender Code-Schnipsel erzeugt einen "dimmbaren Lichtschalter".

```
output:
  - platform: esp8266_pwm
    pin: GPIO0
    frequency: 20000 Hz
    id: pwm_output

light:
  - platform: monochromatic
    output: pwm_output
    name: "heatswitch"
```

Diesen dimmbaren Schalter setze ich zum Heizen auf 75% und ansonsten auf 0% bzw. "Off".


# Nochmal ganz kurz
Hier nochmal in ganz kurz, wie ihr das Ganze aufsetzt, Details finden sich in den Tiefen des Internet.

* Homeassistant aufsetzen
* Smarte Thermostate in HA einbinden
* Platine bestellen, abwarten, bestücken
* ESPHome auf dem ESP installieren und in HA einbinden
* Gehäuse drucken und Platine einbauen
* An die 1-2-4 Schnittstelle anschließen, erst mal ne Weile die gemessene Spannung beobachten...
* TRQ-21 auf Frostschutz stellen und Homeassistant-Script nutzen

# Alternativen
Es gibt diverse Alternativen zu meiner Lösung im Internet, die auf jeden Fall einen Blick wert sind. Und für andere Heizungen bzw. Raum-Temperatur-Regler sind ohnehin andere Lösungen gefragt.

https://blog.pattyland.de/2019/12/01/alte-junkers-gastherme-smart-machen/
https://github.com/RobinMeis/Junkers_1-2-4_ESP32
https://github.com/CWempe/Thermostat-Controller

