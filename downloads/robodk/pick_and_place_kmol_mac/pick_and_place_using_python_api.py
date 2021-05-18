from robolink import *
from robodk import *
 
import os
 
dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)
# Calculate pyramid coordinate
 
# Setup global parameters
BALL_DIAMETER = 100 # diameter of one ball
APPROACH = 100      # approach distance to grab each part, in mm
nTCPs = 6           # number of TCP's in the tool
 
def pyramid_calc(BALLS_SIDE=4):
    """Calculate a list of points (ball center) as if the balls were place in a pyramid"""
    #the number of balls can be calculated as: int(BALLS_SIDE*(BALLS_SIDE+1)*(2*BALLS_SIDE+1)/6)
    #BALL_DIAMETER = 100
    xyz_list = []
    sqrt2 = 2**(0.5)
    for h in range(BALLS_SIDE):
        for i in range(BALLS_SIDE-h):
            for j in range(BALLS_SIDE-h):
                height = h*BALL_DIAMETER/sqrt2 + BALL_DIAMETER/2
                xyz_list = xyz_list + [[i*BALL_DIAMETER + (h+1)*BALL_DIAMETER*0.5, j*BALL_DIAMETER + (h+1)*BALL_DIAMETER*0.5, height]]
    return xyz_list
     
def TCP_On(toolitem, tcp_id):
    """Attach the closest object to the toolitem Htool pose,
    furthermore, it will output appropriate function calls on the generated robot program (call to TCP_On)"""
    toolitem.AttachClosest()
    toolitem.RDK().RunMessage('Set air valve %i on' % (tcp_id+1))
    toolitem.RDK().RunProgram('TCP_On(%i)' % (tcp_id+1));
         
def TCP_Off(toolitem, tcp_id, itemleave=0):
    """Detaches the closest object attached to the toolitem Htool pose,
    furthermore, it will output appropriate function calls on the generated robot program (call to TCP_Off)"""
    toolitem.DetachAll(itemleave)
    toolitem.RDK().RunMessage('Set air valve %i off' % (tcp_id+1))
    toolitem.RDK().RunProgram('TCP_Off(%i)' % (tcp_id+1));
 
# Make a list of positions to place the objects
balls_list = pyramid_calc(4)
 
#print(len(frame1_list))
# 4*4 = 16
# 3*3 = 9
# 2*2 = 4
# 1+4+9+16 = 30
 
# height 50*sqrt(2)
'''
[
 
[50.0, 50.0, 50.0], [50.0, 150.0, 50.0], [50.0, 250.0, 50.0], [50.0, 350.0, 50.0], 
 
[150.0, 50.0, 50.0], [150.0, 150.0, 50.0], [150.0, 250.0, 50.0], [150.0, 350.0, 50.0], 
 
[250.0, 50.0, 50.0], [250.0, 150.0, 50.0], [250.0, 250.0, 50.0], [250.0, 350.0, 50.0], 
 
[350.0, 50.0, 50.0], [350.0, 150.0, 50.0], [350.0, 250.0, 50.0], [350.0, 350.0, 50.0], 
 
 
[100.0, 100.0, 120.71067811865474], [100.0, 200.0, 120.71067811865474], [100.0, 300.0, 120.71067811865474], 
 
[200.0, 100.0, 120.71067811865474], [200.0, 200.0, 120.71067811865474], [200.0, 300.0, 120.71067811865474], 
 
[300.0, 100.0, 120.71067811865474], [300.0, 200.0, 120.71067811865474], [300.0, 300.0, 120.71067811865474], 
 
 
[150.0, 150.0, 191.42135623730948], [150.0, 250.0, 191.42135623730948], 
 
[250.0, 150.0, 191.42135623730948], [250.0, 250.0, 191.42135623730948], 
 
 
[200.0, 200.0, 262.13203435596427]
 
]
 
'''
# https://github.com/RoboDK/RoboDK-API/blob/master/Python/robolink.py
# robodk_path variable to specify location of RoboDK.exe
# under Ubuntu can not use "-NEWINSTANCE"
'''
start_robodk.sh content
LD_LIBRARY_PATH="/home/yen/RoboDK/bin/lib"
export LD_LIBRARY_PATH
/home/yen/RoboDK/bin/RoboDK
'''
RDK = Robolink(robodk_path="/home/yen/start_robodk.sh",args=["-SKIPINI", "-EXIT_LAST_COM"])
# Add robot and the accompanied Base coordinate
print(dir_path + '/Fanuc-M-710iC-50.robot')
# relative directory or absolute directory will work for AddFile under Ubuntu
#robot = RDK.AddFile(r"/home/yen/github/wcm2021/downloads/robodk/pick_and_place_kmol_mac/Fanuc-M-710iC-50.robot")
robot = RDK.AddFile('Fanuc-M-710iC-50.robot')
# Get the default robot base frame
robot_frame = RDK.Item('Fanuc M-710iC/50 Base')
# Move the base frame to the origin
robot_frame.setPose(transl(0,0,0))
 
# Add a tool to an existing robot:
tool = RDK.AddFile(dir_path + '/MainTool.tool', robot)
 
# Add table 1
table1_frame = RDK.AddFrame('Table 1')
table1_frame.setPose(transl(807.766544,-963.699898,41.478944))
table1_stl = RDK.AddFile(dir_path + '/Table.stl', table1_frame)
 
# Add table 2
table2_frame = RDK.AddFrame('Table 2')
table2_frame.setPose(transl(926.465508,337.151529,94.871928))
table2_stl = RDK.AddFile(dir_path + '/Table.stl', table2_frame)
      
# Calculate tool frames for the suction cup tool of 6 suction cups
TCP_list = []
for i in range(nTCPs):
    TCPi_pose = transl(0,0,100)*rotz((360/nTCPs)*i*pi/180)*transl(125,0,0)*roty(pi/2)
    TCPi = robot.AddTool(TCPi_pose, 'TCP %i' % (i+1))
    TCP_list.append(TCPi)
 
TCP_0 = TCP_list[0]
 
# Turn on automatic rendering
RDK.Render(True)
 
# Add balls
# create a list with 30 elements
balls = [None for _ in range(30)]
layer = [16, 9, 4, 1]
count = 0
for i in range(len(balls_list)):
    # transl(balls_list)
    balls[i] = RDK.AddFile('./ball.stl', table1_frame)
    balls[i].setPose(transl(balls_list[i]))
    count = count + 1
    if count <= 16:
        balls[i].setColor([1, 0, 0])
    elif count > 16 and count <= 25:
        balls[i].setColor([0, 1, 0])
    elif count > 25 and count <=29:
        balls[i].setColor([1, 1, 0])
    else:
        balls[i].setColor([0, 0, 1])
 
# Make a list of positions to place the objects
# ball_list is the same as frame1_list
frame1_list = pyramid_calc(4)
frame2_list = pyramid_calc(4)
 
# Move balls 
robot.setPoseTool(TCP_list[0])
nballs_frame1 = len(frame1_list)
nballs_frame2 = len(frame2_list)
idTake = nballs_frame1 - 1
idLeave = 0
idTCP = 0
 
target_app_frame = transl(2*BALL_DIAMETER, 2*BALL_DIAMETER, 4*BALL_DIAMETER)*roty(pi)*transl(0,0,-APPROACH)
 
# frame1 is the same as table1_frame
frame1 = RDK.Item('Table 1')
frame2 = RDK.Item('Table 2')
 
while idTake >= 0:
    # ------------------------------------------------------------------
    # first priority: grab as many balls as possible
    # the tool is empty at this point, so take as many balls as possible (up to a maximum of 6 -> nTCPs)
    ntake = min(nTCPs, idTake + 1)
 
    # approach to frame 1
    robot.setPoseFrame(frame1)
    robot.setPoseTool(TCP_0)
    robot.MoveJ([0,0,0,0,10,-200])
    robot.MoveJ(target_app_frame)
 
    # grab ntake balls from frame1
    for i in range(ntake):
        TCPi = TCP_list[i]
        robot.setPoseTool(TCPi)
        # calculate target wrt frame1: rotation about Y is needed since Z and X axis are inverted
        target = transl(frame1_list[idTake])*roty(pi)*rotx(30*pi/180)
        target_app = target*transl(0,0,-APPROACH)
        idTake = idTake - 1       
        robot.MoveL(target_app)
        robot.MoveL(target)
        TCP_On(TCPi, i)
        robot.MoveL(target_app)
  
    # ------------------------------------------------------------------
    # second priority: unload the tool     
    # approach to frame2 and place the tool balls into table2
    robot.setPoseTool(TCP_0)
    robot.MoveJ(target_app_frame)
    robot.MoveJ([0,0,0,0,10,-200])
    robot.setPoseFrame(frame2)    
    robot.MoveJ(target_app_frame)
    for i in range(ntake):
        TCPi = TCP_list[i]
        robot.setPoseTool(TCPi)
        if idLeave > nballs_frame2-1:
            raise Exception("No room left to place objects in Table 2")
 
        # calculate target wrt frame1: rotation of 180 about Y is needed since Z and X axis are inverted
        target = transl(frame2_list[idLeave])*roty(pi)*rotx(30*pi/180)
        target_app = target*transl(0,0,-APPROACH)
        idLeave = idLeave + 1       
        robot.MoveL(target_app)
        robot.MoveL(target)
        TCP_Off(TCPi, i, frame2)
        robot.MoveL(target_app)
 
    robot.MoveJ(target_app_frame)
 
# Move home when the robot finishes
robot.MoveJ([0,0,0,0,10,-200])