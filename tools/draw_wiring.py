"""Regenerate power and combined diagrams: python tools/draw_wiring.py."""
from pathlib import Path
from html import escape
import subprocess
import sys
import xml.etree.ElementTree as ET
r=Path(__file__).resolve().parents[1]
a=[]
def text(x,y,t,size=20):a.append(f'<text x="{x}" y="{y}" font-family="Arial,sans-serif" font-size="{size}" fill="#193448">{escape(t)}</text>')
def line(x,y,X,Y,c='#303d47'):a.append(f'<path d="M{x},{y} L{X},{Y}" stroke="{c}" stroke-width="3" fill="none"/>')
def box(x,y,w,h):a.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="white" stroke="#45687a" stroke-width="2"/>')
def cap(x,y,label):
 line(x,y,x,y+45);line(x-15,y+45,x+15,y+45);line(x-15,y+55,x+15,y+55);line(x,y+55,x,445);text(x+20,y+75,label,16)
text(35,40,'POWER FIRST | Shared 12 V → L7805 → 5 V VIN',28)
text(35,75,'Logical nets, not hole positions. Verify L7805 TO-220 marking and NodeMCU VIN before connection.',18)
box(35,110,1210,90)
text(55,142,'PHOTO ORIENTATION: NodeMCU USB connector at left',20)
text(55,178,'UPPER red rail = +5 V     LOWER red rail = +12 V     BOTH blue rails = common GND',22)
box(450,245,285,120);text(475,275,'L7805 TO-220',23);text(470,310,'1 IN      2 GND      3 OUT');text(477,342,'Heatsink / tab = GND',18)
line(60,300,450,300,'#c94242');text(60,250,'Lower rail: +12 V',20)
line(735,300,1185,300,'#b26d18');text(810,250,'Upper rail: +5 V → NodeMCU VIN',20)
line(590,365,590,445);line(60,445,1185,445);text(60,480,'Common GND → supply −, both blue rails, NodeMCU GND, driver GND and pump return',20)
cap(180,300,'330 nF / ≥25 V');cap(810,300,'100 nF / ≥16 V')
text(65,525,'Both ceramic capacitors sit directly beside the regulator pins; connect their other ends to GND.',20)
box(35,555,1210,165)
text(55,590,'AT VIN: 10 µF / ≥16 V electrolytic (+ to 5 V, − to GND) and 1k / 0.25 W load (5 V to GND).',20)
text(55,625,'PIN VIEW: printed face toward you, leads down → LEFT 1 IN / CENTER 2 GND / RIGHT 3 OUT.',20)
text(55,660,'Three regulator leads must occupy separate contact strips. Metal-back view reverses left/right.',20)
text(55,695,'Keep the grounded heatsink clear of live pins. Check split rails; never join +12 V to +5 V.',20)
box(35,745,1210,165)
text(55,782,'12 V SUPPLY DISTRIBUTION: fuse branches appropriately; share a common ground point.',21)
text(55,820,'Separate secure wires → A4988 VMOT and pump +12 V; separate power returns to supply −.',20)
text(55,855,'Breadboard +12 V feeds only the regulator branch. Do not route motor/pump current through rails.',20)
text(55,890,'Keep local 100 µF / 25 V bulk capacitors at VMOT and pump switch (see diagrams below).',20)
text(35,955,'3V3 stays separate: NodeMCU 3V3 → A4988 VDD, MS1/2/3, RESET/SLEEP and EN pull-up.',21)
text(35,995,'USB: disconnect external VIN lead before attaching USB; unplug USB before reconnecting VIN.',21)
text(35,1035,'TEST: verify 12 V and 5 V before connecting NodeMCU; then verify its 3V3 and regulator temperature.',20)
text(35,1075,'HEAT: (12 − 5) × load current = 1.4 W at 200 mA, plus internal loss. Validate heatsink under load.',20)
text(35,1115,'Button: D2 to GND only when pressed. Verify tactile-switch pairs by continuity, not appearance.',20)
power='<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="1150" viewBox="0 0 1280 1150"><rect width="1280" height="1150" fill="#f7fafc"/>'+''.join(a)+'</svg>'
(r/'docs/power_wiring.svg').write_text(power)
subprocess.run([sys.executable,str(r/'tools/draw_pump.py')],check=True)
# Standalone diagrams are the source; the combined README image embeds all three.
out=ET.Element('svg',{'xmlns':'http://www.w3.org/2000/svg','width':'1280','height':'3120','viewBox':'0 0 1280 3120'})
y=0
for name,h in [('power_wiring.svg',1150),('stepper_wiring.svg',930),('pump_wiring.svg',1040)]:
 g=ET.SubElement(out,'g',{'transform':f'translate(0 {y})'})
 for el in ET.fromstring((r/'docs'/name).read_text()):g.append(el)
 y+=h
ET.ElementTree(out).write(r/'docs/wiring.svg',encoding='unicode')
