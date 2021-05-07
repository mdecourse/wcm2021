from robodk import *
from robolink import *
        
# Connect to the RoboDK API
RDK = Robolink(robodk_path="C:/robodk522_portable/bin/RoboDK.exe", args=["-NEWINSTANCE", "-SKIPINI", "-EXIT_LAST_COM"])

# Add a reference frame
RDK.AddFrame("參考座標")
# Add robot
robot = RDK.AddFile(r'C:/robodk522_portable/Library/ABB-IRB-120-3-0-6.robot')
# Add stl object
for i in range(500):
    item = RDK.AddFile(r'C:/tmp/untitled.stl')
    # set Pose for item
    item.setPose(rotz(pi/2*i/6)*rotx(pi/5)*transl(200,50*i,900))

# Retrieve all items and print their names (just a reference frame)
list_items = RDK.ItemList()
for item in list_items:
    print(item.Name())   
    
# Close RoboDK
#RDK.CloseRoboDK()