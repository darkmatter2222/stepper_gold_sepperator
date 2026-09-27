"""Generate the inventory-based pump connection diagram (logical pins, not layout)."""
from pathlib import Path
from html import escape
root=Path(__file__).resolve().parents[1]
a=[]
def text(x,y,s,size=19):a.append(f'<text x="{x}" y="{y}" font-family="Arial,sans-serif" font-size="{size}" fill="#193448">{escape(s)}</text>')
def line(x,y,X,Y,color='#234e70'):a.append(f'<path d="M{x},{y} L{X},{Y}" fill="none" stroke="{color}" stroke-width="3"/>')
def box(x,y,w,h):a.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="white" stroke="#45687a" stroke-width="2"/>')
def dot(x,y):a.append(f'<circle cx="{x}" cy="{y}" r="5" fill="#234e70"/>')
def resistor(x,y,w,label):
 box(x,y-18,w,36);text(x+8,y+7,label,17)
text(35,40,'KAMOER 12 V / 5 W • switch built from your inventory',28)
text(35,74,'IRF9540N P-channel + 2N3904 NPN + 1N5822 • D1 HIGH = ON; LOW / reset = OFF',20)
text(35,108,'Logical terminal map: connect the labeled pins. Box positions are NOT physical lead order.',18)
# High-side power path, local reservoir bypass.
text(710,151,'Fused regulated +12 V',20)
line(700,175,1190,175,'#ba3434');line(700,175,700,210,'#ba3434')
box(615,210,210,140);text(635,240,'S • pin 3',18);text(635,275,'Q1 IRF9540N',21);text(635,305,'G • pin 1',18);text(635,333,'D • pin 2 / tab',18)
line(700,350,700,405,'#ba3434');line(700,385,1070,385,'#ba3434');text(830,365,'SWITCHED + (pump +)',18)
box(625,405,150,95);text(645,438,'Kamoer',22);text(647,466,'12 V / 5 W',18);text(680,490,'−',20)
line(700,500,700,660);line(70,660,1190,660);text(580,691,'COMMON GND • supply − / NodeMCU / stepper',20)
# Gate pullup and limited collector connection.
line(510,175,700,175,'#ba3434');line(510,175,510,218)
box(466,218,88,38);text(473,243,'R3 10k',17);line(510,256,510,295);line(510,295,615,295);dot(510,295)
line(400,295,510,295);line(400,295,400,335);box(360,335,80,38);text(367,360,'R4 1k',17);line(400,373,400,445)
box(335,445,195,115);text(354,470,'C',17);text(355,500,'Q2 2N3904',21);text(354,527,'B',17);text(392,549,'E',17)
line(400,560,400,660);dot(400,660)
text(40,460,'NodeMCU',20);text(40,489,'D1 / GPIO5',20)
line(45,520,135,520);resistor(135,520,105,'R1 4.7k');line(240,520,335,520)
line(275,520,275,580);box(230,580,90,38);text(237,605,'R2 100k',17);line(275,618,275,660);dot(275,520);dot(275,660)
# Draw the actual axial diode body with polarity band, avoiding ambiguous symbol art.
line(900,385,900,425);box(884,425,32,85)
a.append('<rect x="885" y="435" width="30" height="9" fill="#234e70"/>')
line(900,510,900,660);dot(900,385);dot(900,660)
text(928,434,'1N5822',18);text(928,463,'BAND ↑',17);text(928,491,'Anode → GND',17)
# Ceramic at pump and supply bulk.
line(1070,385,1070,555);line(1053,555,1087,555);line(1053,570,1087,570);line(1070,570,1070,660)
text(928,600,'100 nF',17);text(928,623,'at pump',17);dot(1070,660)
line(1190,175,1190,280);line(1173,280,1207,280);line(1173,295,1207,295);line(1190,295,1190,660)
text(1163,270,'+',20);text(980,220,'100 µF / 25 V',18);text(980,246,'+ to fused 12 V',17);text(980,272,'− to GND',17)
dot(700,175);dot(700,385);dot(700,660)
box(35,720,1210,150)
text(55,751,'PARTS: 1× IRF9540N, 1× 2N3904, 1× 1N5822; 4.7k, 100k, 10k, 1k resistors (¼ W).',20)
text(55,785,'IRF9540N: printed face toward you, leads down → G / D / S. Metal tab = switched pump +.',19)
text(55,817,'2N3904: typical TO-92 flat face / leads down → E / B / C; verify your actual maker or tester.',19)
text(55,849,'Diode BAND goes to pump + / Q1 drain, NOT the constant +12 V rail. Pump − goes to GND.',19)
text(35,907,'Use existing slow ON/OFF bursts only. This resistor gate drive is not for high-frequency PWM.',20)
text(35,941,'Keep pump current off breadboard rails. Fit flyback diode close to pump; measure startup current.',19)
text(35,975,'Before connecting pump: LOW/reset → gate ≈12 V; HIGH → gate ≈1.3 V (relative to GND).',19)
text(35,1009,'Power NodeMCU through the existing L7805 5 V circuit. Disconnect external VIN before USB.',19)
(root/'docs/pump_wiring.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="1040" viewBox="0 0 1280 1040"><rect width="1280" height="1040" fill="#f7fafc"/>'+''.join(a)+'</svg>')
