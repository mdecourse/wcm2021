from robolink import *    # RoboDK API
from robodk import *      # Robot toolbox
RDK = Robolink()

# Retrieve all targets
targets = RDK.ItemList(ITEM_TYPE_TARGET)

# Select a program (automatic selection if you only have one program)
program = RDK.ItemUserPick('Select a program to check and update targets', ITEM_TYPE_PROGRAM)

# Turn off rendering (faster)
RDK.Render(False)

# List some candidates for the external axis (E1, in mm):
Test_E1 = [500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500]
#test_E1 = range(500, 5000, 500)

for e1 in Test_E1:
   print("Testing program feasibility for E1:" + str(e1))

   # Update all targets to desired e1
   for t in targets:
       # Set the value of the external axis
       # e1 = 5000 # in mm
       t.setJoints([0,0,0,0,0,0, e1])

       # Recalculate the joint position based on the new position of the external axis
       # Robot joints are updated but not external axis
       t.setAsCartesianTarget()
       t.Joints()

       jnts = t.Joints()
       print(t.Name() + "-Joints: " + str(jnts.list()))

   # Test the program and make sure it is 100% feasible
   valid_ins, prog_time, prog_len, valid_ratio, error_msg = program.Update()
   if valid_ratio < 1.0:
       print("  Unable to complete the program")
       print("  " + error_msg)

   else:
       print("  Program feasible!")
       # stop looking
       break

print("Done!")
program.RunProgram()