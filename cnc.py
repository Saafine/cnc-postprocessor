class Woodwop:

    mill_diameter = 16

    def ww_open(self, x, y, z, offX=20, offY=20):
        ww_init = '''[H
VERSION="4.0 Alpha"
HP="1"
IN="0"
GX="0"
BFS="1"
GY="0"
GXY="0"
UP="0"
FM="1"
FW="800"
ZS="20"
HS="4"
OP="4"
MAT="WEEKE"
DN="STANDARD"
INCH="0"
VIEW="NOMIRROR"
ANZ="1"
BES="0"
ENT="0"

[001
x="''' + str(x) + '''"
KM="x"
y="''' + str(y) + '''"
KM="y"
z="''' + str(z) + '''"
KM="z"

<100 \\WerkStck\\
LA="x"
BR="y"
DI="z"
FNX="''' + str(offX / 2) + '''"
FNY="''' + str(offY / 2) + '''"
AX="''' + str(offX) + '''"
AY="''' + str(offY) + '''"
'''
        return str(ww_init)

    def ww_variables(self):
        ww_variables = '''
[001
narz1="132"
KM="nr freza"
pos="5"
KM="posuw"
z1="-3"
KM="glebokosc frezowania"
]
'''
        return ww_variables

    def ww_milling(self):
        ww_milling = ''']1
$E0
KP
X=0.0
Y=0.0
Z=0.0

$E1
KL
X=x
Y=0.0

$E2
KL
X=x
Y=y

$E3
KL
X=0
Y=y

$E4
KL
X=0
Y=0

<105 \\Konturfraesen\\
EA="1:0"
MDA="SEI"
STUFEN="0"
BL="0"
WZS="1"
OSZI="0"
OSZVS="0"
ZSTART="0"
ANZZST="0"
RK="WRKR"
EE="1:4"
MDE="SEI_AB"
EM="0"
RI="1"
TNO="narz1"
SM="0"
S_="STANDARD"
F_="pos"
AB="0"
AF="0"
AW="0"
BW="0"
VLS="0"
VLE="0"
ZA="z1"
SC="0"
HP="0"
SP="0"
YVE="0"
WW="1,2,3,401,402,403"
ASG="2"
KG="0"
RP="STANDARD"
RSEL="0"
RWID="0"
KAT="Fräsen"
MNM="Trimming"
ORI=""
MX="0"
MY="0"
MZ="0"
MXF="1"
MYF="1"
MZF="1"
        '''
        return ww_milling

    def ww_variables_sockle(self):
        ww_variables_sockle = '''
[001
cok_wys="45"
KM="wysokosc cokolu"
cok_gleb="30"
KM="glebokosc cokolu"
cok_r="10"
KM="promien przy cokole"
]
    '''
        return ww_variables_sockle

    def ww_milling_sockle(self, mirror=False):
        if mirror:
            ww_milling_sockle = '''
]1
$E0
KP
X=0.0
Y=0.0
Z=0.0

$E1
KL
X=x-cok_wys
Y=0.0

$E2
KL
X=x
Y=0

$E3
KL
X=x
Y=y-cok_gleb

$E4
KL
X=x-cok_wys
Y=y-cok_gleb

$E5
KR
R=cok_r

$E6
KL
X=x-cok_wys
Y=y

$E7
KL
X=0
Y=y

$E8
KL
X=0
Y=0

<105 \\Konturfraesen\\
EA="1:0"
MDA="SEI"
STUFEN="0"
BL="0"
WZS="1"
OSZI="0"
OSZVS="0"
ZSTART="0"
ANZZST="0"
RK="WRKR"
EE="1:0"
MDE="SEI_AB"
EM="0"
RI="1"
TNO="narz1"
SM="0"
S_="STANDARD"
F_="5"
AB="0"
AF="0"
AW="0"
BW="0"
VLS="0"
VLE="0"
ZA="z1"
SC="0"
HP="0"
SP="0"
YVE="0"
WW="1,2,3,401,402,403"
ASG="2"
KG="0"
RP="STANDARD"
RSEL="0"
RWID="0"
KAT="Fräsen"
MNM="Trimming"
ORI=""
MX="0"
MY="0"
MZ="0"
MXF="1"
MYF="1"
MZF="1"
                            '''
            return ww_milling_sockle
        else:
            ww_milling_sockle = '''
]1
$E0
KP
X=0.0
Y=0.0
Z=0.0

$E1
KL
X=x-cok_wys
Y=0.0

$E2
KL
X=x-cok_wys
Y=cok_gleb

$E3
KR
R=cok_r

$E4
KL
X=x
Y=cok_gleb

$E5
KL
X=x
Y=y

$E6
KL
X=0
Y=y

$E7
KL
X=0
Y=0

<105 \\Konturfraesen\\
EA="1:0"
MDA="SEI"
STUFEN="0"
BL="0"
WZS="1"
OSZI="0"
OSZVS="0"
ZSTART="0"
ANZZST="0"
RK="WRKR"
EE="1:0"
MDE="SEI_AB"
EM="0"
RI="1"
TNO="narz1"
SM="0"
S_="STANDARD"
F_="5"
AB="0"
AF="0"
AW="0"
BW="0"
VLS="0"
VLE="0"
ZA="z1"
SC="0"
HP="0"
SP="0"
YVE="0"
WW="1,2,3,401,402,403"
ASG="2"
KG="0"
RP="STANDARD"
RSEL="0"
RWID="0"
KAT="Fräsen"
MNM="Trimming"
ORI=""
MX="0"
MY="0"
MZ="0"
MXF="1"
MYF="1"
MZF="1"
                '''
            return ww_milling_sockle

    def ww_drilling(self, x, y, diameter, depth):
        ww_drilling = '''
<102 \\BohrVert\\
XA="''' + str(x) + '''"
YA="''' + str(y) + '''"
BM="LS"
TI="''' + str(depth) + '''"
DU="''' + str(diameter) + '''"
AN="1"
MI="0"
S_="1"
XR="1"
YR="0"
ZT="0"
RM="0"
VW="0"
HP="0"
SP="0"
YVE="0"
WW="60,61,62,88,90,91,92,150"
ASG="2"
KAT="Vertical drilling"
MNM="Vertical drilling"
ORI=""
MX="0"
MY="0"
MZ="0"
MXF="1"
MYF="1"
MZF="1"
        '''
        return ww_drilling

    def ww_horizontal_drilling(self, x, y, z, diameter, depth, direction='X+'):
        if direction == 'X+':
            point_towards = 'XP'  # point towards RIGHT
        elif direction == 'X-':
            point_towards = 'XM'  # point towards LEFT

        ww_horizontal_drilling = '''
<103 \BohrHoriz\
MI="0"
XA="'''+str(x)+'''"
YA="'''+str(y)+'''"
ZA="'''+str(z)+'''"
DU="'''+str(diameter)+'''"
TI="'''+str(depth)+'''"
ANA="20"
BM="'''+point_towards+'''"
AN="1"
AB="32"
BM2="STD"
ZT="0"
RM="0"
VW="0"
HP="0"
SP="0"
YVE="0"
WW="50,51,52,53,93,94,95,56,153,151"
ASG="2"
KAT="Horizontalbohren"
MNM="Horizontal drilling"
ORI=""
MX="0"
MY="0"
MZ="0"
MXF="1"
MYF="1"
MZF="1"
KO="00"
        '''
        return ww_horizontal_drilling

    def ww_milling_backwall(self, position, reduced, line='2'): #
        # check for milling side
        if position == 'R':
            start_y = 'y-5'
            mill_side = 'R'
        else:
            start_y = '5'
            mill_side = 'L'

        if reduced == True:  # if backwall goes through entire wall
            start_x = 'x'
            end_x = '0'
            mill_enter = 'SEN'  # SEN -> enter/exit vertical
            mill_exit = 'SEI'  # SEI -> enter/exit tangent
        elif reduced == False:
            start_x = 'x'
            end_x = '0'
            mill_enter = 'SEI'  # SEN -> enter/exit vertical
            mill_exit = 'SEI'  # SEI -> enter/exit tangent
        elif reduced == 'TABLETOP-LEFT':
            start_x = 'x'
            end_x = str(self.mill_diameter / 2 + 5)
            mill_enter = 'SEI'
            mill_exit = 'SEN'  # N -> exit straight up
            mill_side = 'R'
        elif reduced == 'TABLETOP-RIGHT':
            start_x = '0'
            end_x = 'x-' + str(self.mill_diameter / 2 + 5)
            mill_enter = 'SEI'
            mill_exit = 'SEN'  # N -> exit straight up
            mill_side = 'L'
        elif reduced == 'TABLETOP-BOTH':
            start_x = str(self.mill_diameter / 2 + 5)
            end_x = 'x-' + str(self.mill_diameter / 2 + 5)
            mill_enter = 'SEN'
            mill_exit = 'SEN'  # N -> exit straight up
            mill_side = 'L'
        else:  # if reduced number was specified
            start_x = 'x'
            end_x = 'x-'+str(reduced - self.mill_diameter/2 - 5)
            mill_enter = 'SEN'
            mill_exit = 'SEN'



        ww_milling_backwall = '''
]1
$E0
KP
X='''+start_x+'''
Y='''+start_y+'''

$E1
KL
X='''+end_x+'''
Y='''+start_y+'''

<105 \\Konturfraesen\\
EA="'''+line+''':0"
MDA="'''+mill_enter+'''"
STUFEN="0"
BL="0"
WZS="1"
OSZI="0"
OSZVS="0"
ZSTART="0"
ANZZST="0"
RK="WRK'''+mill_side+'''"
EE="'''+line+''':1"
MDE="'''+mill_exit+'''_AB"
EM="0"
RI="1"
TNO="narz1"
SM="0"
S_="STANDARD"
F_="pos"
AB="0"
AF="0"
AW="0"
BW="0"
VLS="0"
VLE="0"
ZA="z/2"
SC="0"
HP="0"
SP="0"
YVE="0"
WW="1,2,3,401,402,403"
ASG="2"
KG="0"
RP="STANDARD"
RSEL="0"
RWID="0"
KAT="Fräsen"
MNM="Trimming"
ORI=""
MX="0"
MY="0"
MZ="0"
MXF="1"
MYF="1"
MZF="1"
        '''
        return ww_milling_backwall

    def ww_sawing(self):
        ww_sawing = '''
<109 \\Nuten \\
XA="0"
YA="14.5"
WI="0"
XE="x"
YE="14.5"
RK="WRKR"
EM="MOD2"
AD="0"
TV="0"
MV="GL"
TI="11"
XY="100"
MN="GGL"
BL="0"
OP="4"
AN="0"
T_="40"
F_="5"
HP="0"
SP="0"
YVE="0"
WW="40,41,42,45,141,142"
ASG="2"
KAT = "Nuten"
MNM = "Grooving"
MX="0"
MY="0"
MZ="0"
MXF="1"
MYF="1"
MZF="1"

<109 \\Nuten \\
XA="0"
YA="15"
WI="0"
XE="x"
YE="15"
RK="WRKR"
EM="MOD2"
AD="0"
TV="0"
MV="GL"
TI="11"
XY="100"
MN="GGL"
BL="0"
OP="4"
AN="0"
T_="40"
F_="5"
HP="0"
SP="0"
YVE="0"
WW="40,41,42,45,141,142"
ASG="2"
KAT = "Nuten"
MNM = "Grooving"
MX="0"
MY="0"
MZ="0"
MXF="1"
MYF="1"
MZF="1"
        '''
        return ww_sawing

    def ww_mill_hole(self, x, y, diameter, depth, line=1):
        ww_mill_hole = '''
]2
$E0
KP
X='''+str(x)+'''
Y='''+str(y)+'''-('''+str(diameter)+'''/2)
Z=0.0
KO=00


$E1
KA
X='''+str(x)+'''
Y='''+str(y)+'''-('''+str(diameter)+'''/2)
DS=3
R='''+str(diameter)+'''/2

<105 \\Konturfraesen\\
EA="'''+str(line)+''':0"
MDA="SEN"
STUFEN="0"
BL="0"
WZS="1"
OSZI="0"
OSZVS="0"
ZSTART="0"
ANZZST="0"
RK="WRKL"
EE="'''+str(line)+''':1"
MDE="SEN_AB"
EM="0"
RI="1"
TNO="narz1"
SM="0"
S_="STANDARD"
F_="5"
AB="0"
AF="0"
AW="0"
BW="0"
VLS="0"
VLE="0"
ZA="z-'''+str(depth)+'''"
SC="0"
HP="0"
SP="0"
YVE="0"
WW="1,2,3,401,402,403"
ASG="2"
KG="0"
RP="STANDARD"
RSEL="0"
RWID="0"
KAT="Fräsen"
MNM="Trimming"
ORI=""
MX="0"
MY="0"
MZ="0"
MXF="1"
MYF="1"
MZF="1"
        '''
        return ww_mill_hole

    def ww_close(self):
        ww_close = '!'
        return ww_close

