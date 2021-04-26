from robolink import *    # API to communicate with RoboDK
from robodk import *      # robodk robotics toolbox
import time

# Any interaction with RoboDK must be done through RDK:
RDK = Robolink()

# get the robot by name:
robot = RDK.Item('', ITEM_TYPE_ROBOT)

# get the home target and the welding targets:
home = RDK.Item('Home')
target = RDK.Item('Target 1')

# get the pose of the target (4x4 matrix representing position and orientation):
poseref = target.Pose()

# move the robot to home, then to the Target 1:
robot.MoveJ(home)
robot.MoveJ(target)

# make an hexagon around the Target 1:
for i in range(7):
    ang = i*2*pi/6 #angle: 0, 60, 120, ...
    for x in [200,210,200]:
        #posei = poseref*rotz(ang)*transl(225,0,0)*rotz(-ang)
        posei = poseref*rotz(ang)*transl(x,0,0)*rotz(-ang)
        robot.MoveL(posei)
        print(posei)
        robot.Pause(.025)

# move back to the center, then home:
robot.MoveL(target)
robot.MoveJ(home)
