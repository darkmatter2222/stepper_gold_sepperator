from pathlib import Path
from html import escape
root=Path(__file__).resolve().parents[1]
a=[]
def text(x,y,s,size=19):a.append(f'<text x="{x}" y="{y}" font-family="Arial,sans-serif" font-size="{size}" fill="#193448">{escape(s)}</text>')
def line(x,y,X,Y,color='#234e70'):a.append(f'<path d="M{x},{y} L{X},{Y}" fill="none" stroke="{color}" stroke-width="3"/>')
def box(x,y,w,h):a.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="white" stroke="#45687a" stroke-width="2"/>')
def dot(x,y):a.append(f'<circle cx="{x}" cy="{y}" r="5" fill="#234e70"/>')
text(35,40,'12 V peristaltic pump · AO3400A low-side switch',28)
text(35,73,'Logical connections; verify breakout pin labels. All ground symbols/nets are connected.',17)
line(700,115,1130,115,'#ba3434');text(710,105,'Regulated +12 V',20)
box(625,155,150,85);text(641,190,'Kamoer pump');text(650,220,'12 V / 5 W')
line(700,115,700,155,'#ba3434');line(700,240,700,285);text(780,265,'Pump − / drain')
box(625,335,150,120);text(640,365,'AO3400A',21);text(644,391,'D = pin 3');text(644,416,'G = pin 1');text(644,443,'S = pin 2')
line(700,285,700,335);line(700,455,700,515);line(460,515,1130,515);text(740,545,'COMMON GND: supply − and NodeMCU GND',19)
box(35,355,220,75);text(50,386,'NodeMCU ESP8266');text(50,413,'D1 / GPIO5')
line(255,402,325,402);box(325,383,105,38);text(337,409,'330 ohm');line(430,402,625,402)
line(495,402,495,445);box(455,445,80,36);text(466,470,'100k');line(495,481,495,515);dot(495,402);dot(495,515)
# Flyback branch: conventional diode triangle-free outline; cathode bar at upper supply side.
line(900,115,900,175);line(880,175,920,175);a.append('<path d="M880,210 L900,175 L920,210 Z" fill="white" stroke="#234e70" stroke-width="3"/>');line(900,210,900,285);line(700,285,1080,285)
text(923,166,'Band / cathode',17);text(923,196,'1N5822',19);text(923,226,'Anode',17);dot(900,115);dot(900,285);dot(700,285)
# Suppression ceramic across motor
line(1080,115,1080,195);line(1060,195,1100,195);line(1060,210,1100,210);line(1080,210,1080,285);dot(1080,115);text(1110,197,'100 nF',16);text(1110,218,'ceramic',16)
text(35,585,'Also add 100 µF / 25 V bulk capacitor: + to 12 V, − to common GND near the switch.',19)
text(35,620,'NodeMCU VIN uses L7805 5 V (see power diagram). Disconnect VIN before USB.',19)
text(35,655,'Use a suitable breakout and secure power wiring; verify startup current and temperature.',19)
text(35,690,'Diode band stays at electrical +12 V even if motor leads are swapped to reverse flow.',19)
body='\n'.join(a)
(root/'docs/pump_wiring.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="730" viewBox="0 0 1280 730"><rect width="1280" height="730" fill="#f7fafc"/>'+body+'</svg>')
