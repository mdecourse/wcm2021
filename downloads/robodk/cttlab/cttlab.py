from robolink import *    # RoboDK API
from robodk import *      # Robot toolbox
RDK = Robolink()

targets = RDK.ItemList(ITEM_TYPE_TARGET)

RDK.Render(False)
for t in targets:
   # Set the value of the external axis
   e1 = 5000 # in mm
   t.setJoints([0,0,0,0,0,0, e1])

   # Recalculate the joint position based on the new position of the external axis
   # Robot joints are updated but not external axis
   t.setAsCartesianTarget()
   t.Joints()

   jnts = t.Joints()
   print(t.Name() + "-Joints: " + str(jnts.list()))