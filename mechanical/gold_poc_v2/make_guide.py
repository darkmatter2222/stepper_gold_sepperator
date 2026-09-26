from pathlib import Path
import math,json
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor,Color,white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from PIL import Image

P=Path(__file__).parent; A=P/'assets'; OUT=P.parent/'Central_Trap_Gold_POC_v2_Assembly.pdf'
pdfmetrics.registerFont(TTFont('DV','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DVB','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
W,H=842,595; ink=HexColor('#20384A'); teal=HexColor('#148895'); gold=HexColor('#D49518'); pale=HexColor('#EDF3F5'); blue=HexColor('#2185BF')
c=canvas.Canvas(str(OUT),pagesize=(W,H));c.setTitle('Central Trap v2 - compact proof-of-concept assembly guide');c.setAuthor('OpenAI / Codex'); page=0
def txt(s,x,y,size=12,bold=False,color=ink):
 c.setFillColor(color);c.setFont('DVB' if bold else 'DV',size);c.drawString(x,y,s)
def para(s,x,y,w,size=12,color=ink):
 st=ParagraphStyle('p',fontName='DV',fontSize=size,leading=size*1.42,textColor=color)
 q=Paragraph(s,st);aw,ah=q.wrap(w,500);q.drawOn(c,x,y-ah);return y-ah
def rect(x,y,w,h,fill=pale,r=10):
 c.setFillColor(fill);c.roundRect(x,y,w,h,r,fill=1,stroke=0)
def pic(name,x,y,w,h):
 p=A/name;im=Image.open(p);iw,ih=im.size;z=min(w/iw,h/ih);dw,dh=iw*z,ih*z
 c.drawImage(str(p),x+(w-dw)/2,y+(h-dh)/2,dw,dh,mask='auto')
def new(title,kicker='BUILD / CENTRAL TRAP v2'):
 global page
 page+=1;c.setFillColor(white);c.rect(0,0,W,H,fill=1,stroke=0)
 txt(kicker,30,565,9,True,teal);txt(title,30,532,24,True)
 c.setStrokeColor(HexColor('#DCE5E9'));c.line(30,518,812,518)
 txt('64 mm bowl  |  Experimental separator  |  Dimensions in mm',30,18,8)
 txt(f'{page:02d}',788,18,10,True)
def end():c.showPage()
def note(s,y=65):
 rect(30,y,782,46);para(s,43,y+34,756,10)
def bolts(x,y,kind='cross',n=4):
 c.setStrokeColor(HexColor('#91A6B2'));c.setLineWidth(1);c.circle(x,y,46,stroke=1,fill=0)
 angles=([0,90,180,270] if kind=='cross' else [45,135,225,315]) if n==4 else [90,210,330]
 for a in angles:
  xx=x+35*math.cos(math.radians(a));yy=y+35*math.sin(math.radians(a));c.setFillColor(blue);c.circle(xx,yy,5,stroke=0,fill=1)
 txt('FASTENER POSITIONS',x-70,y-66,8,True)
def screw(x,y,label,qty):
 c.setStrokeColor(ink);c.setLineWidth(2);c.line(x+10,y,x+70,y);c.rect(x,y-7,10,14,stroke=1,fill=0)
 for i in range(17,69,5):c.line(x+i,y-4,x+i+4,y+4)
 txt(f'{qty} x {label}',x+90,y-4,12,True)
def step(num,title,img,parts,fasteners,actions,check,maptype=None,mapn=4):
 new(f'{num:02d}  {title}')
 rect(30,454,782,50);txt('ADD',43,484,9,True,teal);txt(parts,83,484,11,True);txt(fasteners,83,465,10)
 pic(img,24,91,522,353)
 y=430
 for i,s in enumerate(actions):
  txt(chr(65+i),562,y,12,True,teal);y=para(s,583,y+2,219,11)-17
 if maptype:bolts(685,155,maptype,mapn)
 note('CHECK  '+check,44);end()

new('Central Trap / compact v2','ASSEMBLY GUIDE / SEPTEMBER 2026')
pic('assembly.png',28,68,483,438)
txt('HALF-SIZE BOWL',541,478,15,True,teal)
para('64 mm diameter, reduced from 128 mm. Approximate assembled envelope: <b>86 x 103 x 104 mm</b>, including the drain.',541,450,260,13)
para('A small, modular experiment for central collection of fine heavy particles. Full-size M4 hardware and the NEMA17 motor are retained.',541,348,260,12)
rect(529,152,282,112)
para('<b>Read before printing</b><br/>Check motor dimensions and insert fit on pages 3-4. This revision has analytical screening and CAD checks, not CFD or demonstrated gold recovery.',542,251,252,11)
para('Blue arrows show assembly motion. Gold parts rotate. Teal parts catch water. Rendered screws are replaced by fastener maps and size labels.',541,122,259,10)
end()

new('Printed parts / one small kit')
items=[('P01_base','P01  Base',1),('P02_motor_deck','P02  Motor deck',1),('P03_spacer_x4','P03  Spacer',4),('P04_catcher','P04  Catcher',1),('P05_drive_hub','P05  Drive hub',1),('P06_bowl','P06  Bowl',1),('P07_optional_trap_insert','P07  Optional insert',1),('P08_lid','P08  Cover',1),('P09_insert_coupon','P09  Fit coupon',1)]
for i,(key,label,qty) in enumerate(items):
 col=i%3;row=i//3;x=30+col*263;y=357-row*148
 rect(x,y,252,139);pic(key+'_view0.png',x+5,y+26,241,107);txt(label,x+10,y+10,10,True);txt(f'x{qty}',x+215,y+10,10,True,teal)
end()

new('Hardware / keep these sizes full-size')
rows=[('M4 heat-set inserts',17,'About 6 OD x 6 long; test coupon first'),('M4 x 10 socket screws',4,'Motor deck to base'),('M4 x 25 socket screws',4,'Catcher through spacers into deck'),('M4 x 8 socket screws',7,'3 hub-to-bowl + 4 cover'),('M4 x 10 flat-point set screws',2,'Opposed motor-shaft locking screws'),('M3 x 8 socket screws',4,'Motor mounting; verify thread depth'),('F5-10M / F5-10G thrust bearing',1,'5 bore x 10 OD x 4 overall'),('5 mm shaft NEMA17 motor',1,'Body/mounting assumptions listed below'),('Drain hose + feed tubes','-','18 mm ID drain; 4 mm OD feed tubes')]
y=489
for j,(name,q,use) in enumerate(rows):
 if j%2==0:rect(30,y-26,782,33,fill=pale,r=3)
 txt(name,40,y-12,10,True);txt(str(q),347,y-12,10);txt(use,390,y-12,10);y-=36
para('<b>Motor fit assumption:</b> 42 mm square body, 40 mm body length, 31 mm mounting-hole square, 22 mm pilot no more than 2 mm high. Shaft projection above the mounting face must be about <b>18-26 mm</b>. A 5 mm shaft alone does not verify these dimensions.',40,150,758,11)
para('Also needed: matching hex keys, soldering iron with insert tip, calipers, cable ties, a secondary spill tray, and a current-limited stepper driver/controller. Exact motor current and pinout remain unverified. Do not guess wire pairs or driver current.',40,84,758,10)
end()

new('Prepare / test the inserts before the full print')
pic('P09_insert_coupon_view0.png',26,273,410,221)
txt('5.2    5.4    5.6    5.8    6.0',60,260,16,True,teal)
para('Coupon holes increase in diameter from the small-hole end. Measure to identify them; this view is illustrative. All assembly insert holes are nominally 5.6 mm.',40,241,380,11)
para('Press one insert squarely into the coupon. Let it cool, then test a screw. The insert must hold without cracking or spinning. If another hole size fits better, change INS in build_v2.py and regenerate the parts; do not scale the STL.',40,165,380,11)
txt('INSERT MAP',467,484,13,True,teal)
for j,(a,b) in enumerate([('P01 base','4 / upper ends of posts'),('P02 deck','4 / outer bosses, from above'),('P04 catcher','4 / upper cover bosses'),('P05 hub','2 / opposite radial holes'),('P06 bowl','3 / blind underside holes')]):
 yy=447-j*52;txt(a,468,yy,12,True);txt(b,468,yy-20,11)
para('Seat inserts flush. Keep heat away from bearing seats and the bowl floor. Never drill the bowl holes through into the wet chamber.',468,174,325,11)
note('Before printing: verify motor body, pilot, hole pitch and shaft projection. Unknown motor and insert dimensions are fit assumptions, not measured facts.',44);end()

step(1,'Attach the motor to its deck','step_motor.png','P02 + motor','4 x M3 x 8 socket screws',[
 'Face the motor shaft upward. Put the motor pilot into the recess on the underside of P02.',
 'Install four M3 screws from above the deck. Tighten evenly. Use shorter screws if the motor thread depth is insufficient.'
],'Motor face sits flat. Shaft passes freely through the 5.6 mm opening.','diagonal')
step(2,'Lower the motor into the base','step_base.png','P01 + motor/deck assembly','4 x M4 x 10 socket screws',[
 'Lower the motor between the four base posts. Align the four inner deck holes with the post inserts.',
 'Run the cable out through an open side. Tie it to the two base slots, clear of the shaft and drain side.',
 'Install the four M4 screws. Secure the base to the bench through its spare mounting holes.'
],'Motor clears the base floor; wires are not pinched.','cross')
step(3,'Stack the thrust bearing','step_bearing.png','1 x complete 5 x 10 x 4 thrust bearing','No screws in this step',[
 'Slide the lower housing washer onto the central pedestal, followed by the ball cage and upper shaft washer.',
 'Bearing grooves face the balls. Use the bearing maker\'s orientation; the housing washer typically has the slightly larger bore.',
 'The upper washer turns with the hub. This bearing carries axial load; the motor still guides the rotor radially.'
],'Bearing stack sits flat on the pedestal and turns freely.')
step(4,'Build the rotor outside the machine','step_hub.png','P05 hub + P06 bowl','3 x M4 x 8 socket screws; 2 x M4 x 10 set screws',[
 'Align the three hub flange holes with the three dry inserts under the bowl.',
 'Insert the three M4 x 8 screws from below the hub flange. Tighten evenly without distorting the bowl.',
 'Start both radial set screws in the hub. Back them out until the shaft bore is unobstructed.'
],'No screw enters the water chamber. Keep this rotor aside for step 7.','cross',3)
step(5,'Set the four spacers','step_spacers.png','4 x P03 spacers','No screws yet',[
 'Place one 12 mm spacer on each of the four outer deck bosses.',
 'Align the spacer holes with the inserts below. Keep the bearing and motor shaft clean.'
],'All four spacers sit upright and flat.','diagonal')
step(6,'Mount the catcher','step_catcher.png','P04 catcher','4 x M4 x 25 socket screws',[
 'Lower the catcher onto the four spacers. Point the drain toward your collection hose.',
 'Pass each screw through a lower catcher tab and spacer into a deck insert. Tighten in alternating pairs.',
 'The large central opening stays open for installation of the rotor. Keep the upper cover inserts empty.'
],'Four spacers are trapped squarely. The catcher is stationary.','diagonal')
step(7,'Seat and lock the rotor','step_bowl.png','Preassembled P05 + P06 rotor','Tighten the 2 opposed M4 set screws',[
 'Lower the rotor onto the 5 mm shaft. Its hub nose rests on the upper thrust-bearing washer.',
 'Reach the two set screws through the gap below the catcher. Tighten evenly with a straight hex key; do not force axial preload.',
 'Turn the bowl by hand through a full revolution. Stop if it rubs, rocks or binds. Adjust fit before powering.'
],'Nominal skirt clearance: 1.3 mm radial, 1 mm vertical. Real print runout must fit inside it.')
step(8,'Fit the cover and water lines','step_lid.png','P08 cover + hose + feed tube','4 x M4 x 8 socket screws',[
 'Install the cover on the four upper catcher bosses. Tighten the four screws lightly and evenly.',
 'Secure feed tubing in the 4.3 mm ports. Keep tube ends at least 3 mm above the highest bowl rim; stop them from sliding downward.',
 'Connect a drain hose to the 18 mm OD spout. Support the hose so it cannot twist the printed spout.'
],'Feed opening is 26 mm. The lid is a splash cover, not a sealed pressure lid.','diagonal')

new('Water path / floor-level drain')
pic('section_P04_catcher.png',24,141,515,363)
txt('SECTION THROUGH CATCHER',51,124,10,True,teal)
para('<b>1 / Overflow</b><br/>Water passes over the bowl rim into the stationary catcher. The rotating bowl itself has a continuous wet wall and floor.',556,481,247,12)
para('<b>2 / Sloped floor</b><br/>The catcher floor falls 3% toward the drain. The flat-bottomed outlet follows that slope, with no designed raised sill.',556,370,247,12)
para('<b>3 / Downhill outlet</b><br/>Run the hose continuously downhill into a second container. A blocked outlet can flood the central shaft opening and motor.',556,257,247,12)
note('Leak-test bowl and catcher separately before assembly. Closed STL geometry does not make an FDM print watertight. Inspect seams and coat/reprint if needed.',44);end()

new('Central sump / start without the optional insert')
pic('section_P06_bowl.png',24,179,448,316)
pic('step_insert.png',510,266,283,230)
para('<b>Open sump - first test</b><br/>The 16 mm sump has a smooth rounded entrance and roughly 1.7 mL of deep pocket volume. There is no raised collar across the working slope. The slope may help migration only when grains can actually slip or be mobilized.',39,168,407,11)
para('<b>P07 - later A/B test only</b><br/>Three feet rest on the sump floor. The cone remains below the entrance; its central opening is 10 mm. It is gravity-seated, not locked. Omit it if warped, loose or lifting during a test.',500,246,293,11)
para('A pocket can trap sand and clay as well as gold. This is not a one-way valve and cannot guarantee that fine gold stays in. Inspect and clean it frequently.',500,123,293,11)
end()

new('Printing / use the delivered orientations')
para('STLs are in millimeters and already oriented for printing. Print one of each file, except P03: print four. Do not apply 50% scaling in the slicer; the redesign is already reduced.',38,491,764,12)
rows=[('P01','Base down','Brim helps tall posts; keep post bores clean'),('P02','Deck inverted','Support broad deck face around the 2 mm bearing pedestal'),('P03','Spacer upright','No support normally needed'),('P04','Catcher upright','Support spout, lower body and projecting upper bosses'),('P05','Flange down','Keep shaft bore and radial insert bores clear'),('P06','Bowl upright','Support external flare and underside skirt; protect wet face'),('P07','Cone inverted','Fine layers; delicate legs; experimental part'),('P08','Cover flat','No support normally needed'),('P09','Coupon flat','Print first using the intended final material/settings')]
y=409
for i,(a,b,d) in enumerate(rows):
 if i%2==0:rect(30,y-25,782,34,r=3)
 txt(a,40,y-12,11,True);txt(b,95,y-12,11);txt(d,300,y-12,10);y-=35
para('<b>Starting settings:</b> PETG, 0.20 mm layers, 5-6 perimeters, 6-8 top/bottom layers, 40-60% infill. Use 0.12-0.16 mm layers for P07. These are starting points, not a waterproofing certification. Remove supports and strings; keep paired rotating hardware equal.',39,82,765,10)
end()

new('Commission / measure losses before adding more feed')
steps=[('A  DRY FIT','Hand-turn a full revolution. Check shaft grip, bearing seating, cover clearance and cable routing. Keep a spill tray underneath.'),('B  WATER ONLY','Start with small oscillations, about +/-3 to 5 degrees at 0.5-1 Hz. Use smooth acceleration. Check leakage and rubbing. These are exploratory commands, not a motor rating.'),('C  SMALL SAMPLE','Wet-screen and disperse clay. Begin with 0.5-2 g of screened sand, not a full hopper. Try 5-30 mL/min water after filling, then adjust to obtain gentle overflow. Stop if material packs or the drain backs up.'),('D  KEEP EVERY TAILING','Use separate containers for overflow and final concentrate. Rinse and inspect both. Test with known-size gold only after mechanical tests; quantify losses by size class.'),('E  CHANGE ONE VARIABLE','Compare open sump to optional insert; record water, frequency, angle, sample mass and run time. Delay any spin/ejection experiments until baseline recovery is measured.')]
y=481
for h,b in steps:
 txt(h,40,y,12,True,teal);y=para(b,245,y+2,545,11)-25
note('No unattended continuous-feed claim: capacity, clay handling, recovery and safe motor settings are unproven. Never discard test tailings. No controller or automatic feeder is included.',44);end()

new('Mechanics / what has and has not been modeled')
txt('ANALYTICAL SCREENING',40,482,12,True,teal)
para('The working slope is approximately 20.2 degrees. Rotation produces outward acceleration a = omega squared x radius. At 30 rpm and a 29 mm radius, this is about 0.029 g. Faster spinning increasingly opposes travel toward the center.',40,460,365,11)
para('A simplified particle sliding down a rotating cone requires:<br/><b>omega squared x r / g &lt; (tan(beta) - mu) / (1 + mu tan(beta))</b><br/>Here mu is sliding friction. The ideal dry-contact model omits drag, bed interactions and transient water motion. Density cancels: this is not a gold-selection rule.',40,353,365,11)
para('Calculated inward-sliding limits at 29 mm radius:<br/>mu = 0: 107 rpm; 0.1: 89 rpm;<br/>0.2: 70 rpm; 0.3: 44 rpm.<br/>At mu = 0.4, the model predicts no spontaneous inward sliding even at rest. These are not operating speed limits.',40,226,365,11)
txt('FINE PARTICLES NEED TIME',446,482,12,True,teal)
para('Stokes settling gives v = (rho particle - rho water) g d squared / (18 viscosity). A spherical 10 micrometer gold grain in clean water needs roughly 5 seconds to fall 5 mm; a 20 micrometer sphere needs about 1.25 seconds.',446,460,356,11)
para('At five times the viscosity, those times become about 25 and 6.3 seconds. Real clay slurry may be non-Newtonian; gold flakes, attached clay and a moving particle bed are outside this simple model.',446,342,356,11)
para('Published tea-leaf-paradox studies support possible inward near-bottom transport under some rotating-flow conditions. They also show sensitivity to geometry and confinement. They do not establish this device as a gold concentrator.',446,240,356,11)
note('No CFD, particle-transport simulation or bench recovery test was performed. Bowl angle and sump geometry are testable choices, not an identified optimum or a guarantee.',44);end()

new('Review record / references and revision notes')
txt('GEOMETRY REVIEW',40,483,12,True,teal)
para('All 9 STLs were rendered and visually reviewed from top-oblique, underside-oblique and front views. The bowl and catcher were also sectioned. The package includes these review sheets.',40,460,365,11)
para('Every exported STL passed closed-edge, consistent-orientation and positive-volume checks. All CAD parts are valid single solids. The modeled assembly has no detected interference; the rotor was checked every 15 degrees. This does not measure print tolerance, physical balance or recovery.',40,363,365,11)
para('<b>Changed from v1:</b> 64 mm bowl; shorter direct-shaft drive with a thrust bearing; round mounting bosses; sloped catcher floor and floor-level D-shaped drain; smooth open sump entry; optional recessed insert. The 18 mm hose connection and M4 hardware remain full-size.',40,229,365,11)
txt('PRIMARY REFERENCES',446,483,12,True,teal)
refs=[('Rotating-flow / bottom inclination study, Micromachines 14(11), article 2024 (2023).','https://www.mdpi.com/2072-666X/14/11/2024'),('Stepper-driven cup / particle aggregation study, volume 4(3), article 37 (2024).','https://www.mdpi.com/2673-8716/4/3/37'),('SMB Bearings: F5-10G dimension drawing (5 x 10 x 4 mm).','https://www.smbbearings.com/firebrick/ckeditor/plugins/upload/Uploads/Documents/bearingpdfs/F5-10G-thrust-bearing-5x10x4mm.pdf'),('US EPA: gravity concentration, feed preparation and recovery context.','https://www.epa.gov/international-cooperation/artisanal-and-small-scale-gold-mining-without-mercury')]
y=460
for i,(label,url) in enumerate(refs):
 y=para(f'{i+1}. {label}<br/><link href="{url}" color="#148895">Open primary source</link>',446,y,354,10)-17
para('Sources explain mechanisms and hardware dimensions. None validates this prototype. Exact Moons C17HD40-102-0 1N ratings were not verified.',446,y,354,10)
note('Files: STL print parts; STEP geometry; assembly.step; build_v2.py; check reports; multi-view review sheets. Re-run the generator after changing motor or insert dimensions.',44);end()
c.save();print(OUT);print('Pages',page)
