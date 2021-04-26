from robolink import *                  # import the robolink library
from robodk import *                    # import the robodk library
 
RDK = Robolink()                        # connect to the RoboDK API
robot  = RDK.Item('', ITEM_TYPE_ROBOT)  # Retrieve a robot available in RoboDK
#target  = RDK.Item('Target 1')         # Retrieve a target (example)
 
 
pose = robot.Pose()                     # retrieve the current robot position as a pose (position of the active tool with respect to the active reference frame)
# target = target.Pose()                # the same can be applied to targets (taught position)
 
# Read the 4x4 pose matrix as [X,Y,Z , A,B,C] Euler representation (mm and deg): same representation as KUKA robots
XYZABC = Pose_2_KUKA(pose)
print(XYZABC)
 
# Read the 4x4 pose matrix as [X,Y,Z, q1,q2,q3,q4] quaternion representation (position in mm and orientation in quaternion): same representation as ABB robots (RAPID programming)
xyzq1234 = Pose_2_ABB(pose)
print(xyzq1234)
 
# Read the 4x4 pose matrix as [X,Y,Z, u,v,w] representation (position in mm and orientation vector in radians): same representation as Universal Robots
xyzuvw = Pose_2_UR(pose)
print(xyzuvw)
 
x,y,z,a,b,c = XYZABC                    # Use the KUKA representation (for example) and calculate a new pose based on the previous pose
XYZABC2 = [x,y,z+50,a,b,c+45]
pose2 = KUKA_2_Pose(XYZABC2)            # Convert the XYZABC array to a pose (4x4 matrix)
 
robot.MoveJ(pose2)                      # Make a joint move to the new position
# target.setPose(pose2)                  # We can also update the pose to targets, tools, reference frames, objects, ...