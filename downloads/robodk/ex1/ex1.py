from robolink import *              # import the robolink library (bridge with RoboDK)
from robodk import *                # import the robodk library (robotics toolbox)
 
RDK = Robolink()                    # establish a link with the simulator
robot = RDK.Item('KUKA KR 210 L100-2 K')      # retrieve the robot by name
robot.setJoints([0,-90,90,0,0,0])   # set the robot to the home position
 
target = robot.Pose()               # retrieve the current target as a pose (position of the active tool with respect to the active reference frame)
xyzabc = Pose_2_KUKA(target)        # Convert the 4x4 pose matrix to XYZABC position and orientation angles (mm and deg)
 
x,y,z,a,b,c = xyzabc                # Calculate a new pose based on the previous pose
xyzabc2 = [x,y,z+50,a,b,c+45]
target2 = KUKA_2_Pose(xyzabc2)      # Convert the XYZABC array to a pose (4x4 matrix)
 
robot.MoveJ(target2)                # Make a linear move to the calculated position