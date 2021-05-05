# Copyright 2015-2019 - RoboDK Inc. - https://robodk.com/
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# ----------------------------------------------------
# This file is a sample POST PROCESSOR script to generate robot programs for a B&R Automation controller
#
# To edit/test this POST PROCESSOR script file:
# Select "Program"->"Add/Edit Post Processor", then select your post or create a new one.
# You can edit this file using any text editor or Python editor. Using a Python editor allows to quickly evaluate a sample program at the end of this file.
# Python should be automatically installed with RoboDK
#
# You can also edit the POST PROCESSOR manually:
#    1- Open the *.py file with Python IDLE (right click -> Edit with IDLE)
#    2- Make the necessary changes
#    3- Run the file to open Python Shell: Run -> Run module (F5 by default)
#    4- The "test_post()" function is called automatically
# Alternatively, you can edit this file using a text editor and run it with Python
#
# To use a POST PROCESSOR file you must place the *.py file in "C:/RoboDK/Posts/"
# To select one POST PROCESSOR for your robot in RoboDK you must follow these steps:
#    1- Open the robot panel (double click a robot)
#    2- Select "Parameters"
#    3- Select "Unlock advanced options"
#    4- Select your post as the file name in the "Robot brand" box
#
# To delete an existing POST PROCESSOR script, simply delete this file (.py file)
#
# ----------------------------------------------------
# More information about RoboDK Post Processors and Offline Programming here:
#     https://robodk.com/help#PostProcessor
#     https://robodk.com/doc/en/PythonAPI/postprocessor.html
# ----------------------------------------------------

#RoboDK python file header
ROBODK_PYTHON_HEDAER = """# Type help("robolink") or help("robodk") for more information
# Press F5 to run the script
# Documentation: https://robodk.com/doc/en/RoboDK-API.html
# Reference:     https://robodk.com/doc/en/PythonAPI/index.html
# Note: It is not required to keep a copy of this file, your python script is saved with the station
from robolink import *    # RoboDK API
from robodk import *      # Robot toolbox
RDK = Robolink()
"""

ROBODK_API_SAFE_MOVE_HEADER = """
def MoveJAPISafe(pose):
    robot.MoveJ(pose,True)
    status, status_msg = robot.ConnectedState()
    if status != ROBOTCOM_READY:
        # Stop if the connection did not succeed
        print(status_msg)
        raise Exception("Robot driver error: " + status_msg)

def MoveLAPISafe(pose):
    robot.MoveL(pose,True)
    status, status_msg = robot.ConnectedState()
    if status != ROBOTCOM_READY:
        # Stop if the connection did not succeed
        print(status_msg)
        raise Exception("Robot driver error: " + status_msg)

def MoveCAPISafe(pose1,pose2):
    robot.MoveC(pose1,pose2,True)
    status, status_msg = robot.ConnectedState()
    if status != ROBOTCOM_READY:
        # Stop if the connection did not succeed
        print(status_msg)
        raise Exception("Robot driver error: " + status_msg)
"""

# ----------------------------------------------------
# Import RoboDK tools

from robodk import *      # Robot toolbox

# ----------------------------------------------------
def pose_2_str(pose, joints = None):
    """Prints a pose target"""
    if pose is None:
        pose = eye(4)
    x,y,z,rx,ry,rz = pose.Pose_2_TxyzRxyz()
    str_xyzwpr = 'Pose(%.3f, %.3f, %.3f,  %.3f, %.3f, %.3f)' % (x,y,z,rx*180/pi,ry*180/pi,rz*180/pi)
    return str_xyzwpr

def mat_2_str(mat):
    returnString = str(mat).split(":\n")[0]
    return returnString

def joints_2_str(joints):
    """Prints a joint target"""
    if joints is None:
        return ""
        
    str = ''
    for i in range(len(joints)):
        str = str + ('%.6f,' % (joints[i]))
    str = str[:-1]
    return str

# Parent: make sure the parent matches
def PoseDistance(pose1, pose2):
    """0.000001"""
    distance_mm = distance(pose1.Pos(), pose2.Pos())
    distance_deg = pose_angle_between(pose1, pose2) * 180 / pi
    return distance_mm + distance_deg



# ----------------------------------------------------    
# Object class that handles the robot instructions/syntax
class RobotPost(object):
    """Robot post object"""   
    
    #Code generation mode
    # 1 = simulate
    # 2 = Online Programming (run on robot)
    # 3 = Macro generation (RDK.AddProgram)
    POST_CODEGEN_MODE = 3

    #Name of the main function, obtained from first instance of ProgStart being called
    MAIN_PROGRAM_NAME = None

    #Name of the current program being written, only for AddProgram (mode 3)
    #Defaults to robot for api usage (mode 1 and 2)
    CURRENT_PROGRAM_NAME = 'robot'
    
    #----------------------------------------------------
    if POST_CODEGEN_MODE == 3:
        CURRENT_PROGRAM_NAME = 'program'
    
    #Unique Target Couter
    TARGET_COUNT = 0

    # other variables
    PROG_EXT = 'py'        # set the program extension
    ROBOT_POST = ''
    ROBOT_NAME = ''
    PROG_FILES = []
    
    PROG = ''
    LOG = ''
    nAxes = 6
    REF_FRAME = eye(4)

    #Need to make the robot object here
    def __init__(self, robotpost=None, robotname=None, robot_axes = 6, **kwargs):
        self.ROBOT_POST = robotpost
        self.ROBOT_NAME = robotname
        self.PROG = ''
        self.LOG = ''
        self.nAxes = robot_axes

        self.addline(ROBODK_PYTHON_HEDAER)

        varname = FilterName(robotname).replace('.', '')

        self.addline('#Robot object creation')
        self.addline('robot = RDK.Item("%s", ITEM_TYPE_ROBOT)' % (robotname))
        self.addline('if not robot.Valid():')
        self.addline('    raise Exception(\'Could not find robot %s\')' % (robotname) )
        self.addline('')
        if self.POST_CODEGEN_MODE == 3:
            #You only need the robots reference when generating programs
            self.addline('#Robot frame creation')
            self.addline('robotFrame = robot.Parent()')
            self.addline('if robotFrame.Type() != ITEM_TYPE_FRAME:')
            self.addline('    raise Exception(\'Robot parent is not a frame\')')
                


        if self.POST_CODEGEN_MODE == 2:
            #Define function for run on robot 
            self.addline(ROBODK_API_SAFE_MOVE_HEADER)
        
            self.addline('#robot.Disconnect()')
            self.addline('robot.Connect() # Try to connect')
            self.addline('import time')
            self.addline('time.sleep(2.0) #Just in case the driver is not done starting')
            self.addline('status, status_msg = robot.ConnectedState()')
            self.addline('if status != ROBOTCOM_READY:')
            self.addline('    # Stop if the connection did not succeed')
            self.addline('    print(status_msg)')
            self.addline('    raise Exception("Failed to connect: " + status_msg)')
            self.addline('# This will set to run the API programs on the robot and the simulator (online programming)')
            self.addline('RDK.setRunMode(RUNMODE_RUN_ROBOT)')

        self.addline('')
        self.addline('')

        for k,v in kwargs.items():
            if k == 'lines_x_prog':
                self.MAX_LINES_X_PROG = v       
        
    def ProgStart(self, progname):
        prognamesafe = FilterName(progname).replace('.', '')
        str_axes = ''
        for i in range(self.nAxes):
            str_axes += ',J%i (deg)' % (i+1)
        if self.MAIN_PROGRAM_NAME is None:
            self.MAIN_PROGRAM_NAME = prognamesafe
        self.addline('')    
        self.addline('# Program Start,' + prognamesafe)
        self.addline('def ' + prognamesafe + '():')
        
        if self.POST_CODEGEN_MODE == 3:
            self.addline('    # Create program item for: ' + prognamesafe)
            self.addline('    %s = RDK.Item(\'%s\',ITEM_TYPE_PROGRAM)' % (prognamesafe,progname))    
            self.addline('    if %s.Valid():' % prognamesafe)    
            if self.MAIN_PROGRAM_NAME !=prognamesafe:            
                #Dont rerun the adding code if the function already exists
                self.addline('        #Program with name %s already exists, skipping function generation)' % prognamesafe)
                self.addline('        return')    
            else:
                self.addline('        raise Exception(\'Program with name %s already exists.\')' % prognamesafe)    

            self.CURRENT_PROGRAM_NAME = prognamesafe
            self.addline('    %s = RDK.AddProgram(\'%s\')' % (prognamesafe,progname) )
            self.addline('    %s.setParam("Tree","collapse")' % (prognamesafe) )
            self.addline('')
            
        
    def ProgFinish(self, progname):
        self.addline('    return')
        
    def ProgSave(self, folder, progname, ask_user=False, show_result=False):
        if self.MAIN_PROGRAM_NAME is not None:
            self.addline('')
            self.addline('#Call main')
            self.addline(self.MAIN_PROGRAM_NAME + '()')
            

        progname = progname + '.' + self.PROG_EXT
        if ask_user or not DirExists(folder):
            filesave = getSaveFile(folder, progname, 'Save program as...')
            if filesave is not None:
                filesave = filesave.name
            else:
                return
        else:
            filesave = folder + '/' + progname
        fid = open(filesave, "w")
        fid.write(self.PROG)
        fid.close()
        print('SAVED: %s\n' % filesave)
        self.PROG_FILES = filesave
        #---------------------- show result
        if show_result:
            if type(show_result) is str:
                # Open file with provided application
                import subprocess
                p = subprocess.Popen([show_result, filesave])   
            elif type(show_result) is list:
                import subprocess
                p = subprocess.Popen(show_result + [filesave])   
            else:
                # open file with default application
                import os
                os.startfile(filesave)  
            
            if len(self.LOG) > 0:
                mbox('Program generation LOG:\n\n' + self.LOG)
    
    def ProgSendRobot(self, robot_ip, remote_path, ftp_user, ftp_pass):
        """Send a program to the robot using the provided parameters. This method is executed right after ProgSave if we selected the option "Send Program to Robot".
        The connection parameters must be provided in the robot connection menu of RoboDK"""
        UploadFTP(self.PROG_FILES, robot_ip, remote_path, ftp_user, ftp_pass)
        
    def MoveJ(self, pose, joints, conf_RLF=None):
        """Add a joint movement"""
        if pose is not None:
            self.addline('    #MoveJ ' + mat_2_str(pose))
            if self.POST_CODEGEN_MODE == 1:
                self.addline('    %s.MoveJ(%s,True)' % (self.CURRENT_PROGRAM_NAME,mat_2_str(pose)) )
            if self.POST_CODEGEN_MODE == 2:
                self.addline('    MoveJAPISafe(%s)' % mat_2_str(pose))
            if self.POST_CODEGEN_MODE == 3:
                varNameTarget = FilterName('AutoTarget %i' % self.TARGET_COUNT)
                self.addline('    %s = RDK.AddTarget(\'AutoTarget %i\',robotFrame,robot)' % (varNameTarget,self.TARGET_COUNT) )
                self.addline('    %s.setPose(%s)' %  (varNameTarget,mat_2_str(pose)) )
                self.addline('    %s.MoveJ(%s,True)' % (self.CURRENT_PROGRAM_NAME,varNameTarget) )
                self.TARGET_COUNT += 1
        else:
            self.addline('    #MoveJ ' + joints_2_str(joints))
            if self.POST_CODEGEN_MODE == 1:
                self.addline('    %s.MoveJ([%s],True)' % (self.CURRENT_PROGRAM_NAME,joints_2_str(joints)) )
            if self.POST_CODEGEN_MODE == 2:
                self.addline('    MoveJAPISafe([%s])' % joints_2_str(joints))
            if self.POST_CODEGEN_MODE == 3:
                varNameTarget = FilterName('AutoTarget %i' % self.TARGET_COUNT)
                self.addline('    %s = RDK.AddTarget(\'AutoTarget %i\',robotFrame,robot)' % (varNameTarget,self.TARGET_COUNT) )
                self.addline('    %s.setJoints(%s)' %  (varNameTarget,joints_2_str(joints)) )
                self.addline('    %s.MoveJ(%s,True)' % (self.CURRENT_PROGRAM_NAME,varNameTarget) )
                self.TARGET_COUNT += 1
                


    def MoveL(self, pose, joints, conf_RLF=None):
        """Add a linear movement"""
        pose_abs = self.REF_FRAME * pose
        self.addline('    #MoveL ' + mat_2_str(pose))
        if self.POST_CODEGEN_MODE == 1:
            self.addline('    %s.MoveL(%s,True)' % (self.CURRENT_PROGRAM_NAME,mat_2_str(pose)) )      
        if self.POST_CODEGEN_MODE == 2:
            self.addline('    MoveLAPISafe(%s)' % mat_2_str(pose))      
        if self.POST_CODEGEN_MODE == 3:
            varNameTarget = FilterName('AutoTarget %i' % self.TARGET_COUNT)
            self.addline('    %s = RDK.AddTarget(\'AutoTarget %i\',robotFrame,robot)' % (varNameTarget,self.TARGET_COUNT) )
            self.addline('    %s.setPose(%s)' %  (varNameTarget,mat_2_str(pose)) )
            self.addline('    %s.MoveL(%s,True)' % (self.CURRENT_PROGRAM_NAME,varNameTarget) )
            self.TARGET_COUNT += 1
        
    def MoveC(self, pose1, joints1, pose2, joints2, conf_RLF_1=None, conf_RLF_2=None):
        """Add a circular movement"""    
        self.addline('    #MoveC ' + mat_2_str(pose1) + ' , ' + mat_2_str(pose2))
        if self.POST_CODEGEN_MODE == 1:
            self.addline('    %s.MoveC(%s,%s,True)' % (self.CURRENT_PROGRAM_NAME,mat_2_str(pose2),mat_2_str(pose1)) )        
        if self.POST_CODEGEN_MODE == 2:
            self.addline('    MoveCAPISafe(%s,%s)' % (mat_2_str(pose2),mat_2_str(pose1)) )        
        if self.POST_CODEGEN_MODE == 3:
            varNameTarget1 = FilterName('AutoTarget %i' % self.TARGET_COUNT)
            varNameTarget2 = FilterName('AutoTarget %i' % (self.TARGET_COUNT+1) )
            self.addline('    %s = RDK.AddTarget(\'AutoTarget %i\',robotFrame,robot)' % (varNameTarget1,self.TARGET_COUNT) )
            self.addline('    %s.setPose(%s)' %  (varNameTarget1,mat_2_str(pose1)) )
            self.addline('    %s = RDK.AddTarget(\'AutoTarget %i\',robotFrame,robot)' % (varNameTarget2,self.TARGET_COUNT+1) )
            self.addline('    %s.setPose(%s)' %  (varNameTarget2,mat_2_str(pose2)) )
            self.addline('    %s.MoveC(%s,%s,True)' % (self.CURRENT_PROGRAM_NAME,varNameTarget2,varNameTarget1) )        
            self.TARGET_COUNT += 2

    def setFrame(self, pose, frame_id=None, frame_name=None):
        """Change the robot reference frame"""
        self.REF_FRAME = pose
        varname = FilterName(frame_name).replace('.', '')
        self.addline('    #Set frame %s' % frame_name)
        self.addline('    %s = RDK.Item("%s", ITEM_TYPE_FRAME)' % (varname, frame_name))
        self.addline('    if not %s.Valid():' % varname)
        self.addline('        %s = RDK.AddFrame("%s")' % (varname,frame_name) )
        self.addline('        %s.setPose(%s)' % (varname,mat_2_str(pose)) )
        if self.POST_CODEGEN_MODE == 3:
            self.addline('        %s.setParent(\'robotFrame\')' % varname )
        self.addline('    %s.setPoseFrame(%s)' % (self.CURRENT_PROGRAM_NAME,varname) )
        self.addline('')        
        
        
    def setTool(self, pose, tool_id=None, tool_name=None):
        """Change the robot TCP"""
        if tool_name != '':
            varname = FilterName(tool_name).replace('.', '')
            self.addline('    #Set Tool by name ' + tool_name)
            self.addline('    %s = RDK.Item("%s", ITEM_TYPE_TOOL)' % (varname, tool_name))
            self.addline('    if %s.Valid():' % varname)
            self.addline('        %s.setPoseTool(%s)' % (self.CURRENT_PROGRAM_NAME,varname) )
            self.addline('    else:')
            self.addline('        %s.setPoseTool(%s)' % (self.CURRENT_PROGRAM_NAME,mat_2_str(pose)) )
        else:
            self.addline('    #Set Tool by pose ' + mat_2_str(pose))
            self.addline('    %s.setPoseTool(%s),' % (self.CURRENT_PROGRAM_NAME,mat_2_str(pose)) )
        self.addline('')


    def Pause(self, time_ms):
        """Pause the robot program"""
        if time_ms < 0:
            self.addline('    RDK.ShowMessage(\'STOP\',True)')
        else:
            self.addline('    import time')
            self.addline('    time.sleep(%.3f)' % (time_ms*1000))
    
    def setSpeed(self, speed_mms):
        """Changes the robot speed (in mm/s)"""
        varname = FilterName(self.ROBOT_NAME).replace('.', '')
        self.addline('    %s.setSpeed(%s,-1,-1,-1)' % (self.CURRENT_PROGRAM_NAME,str(speed_mms)))

    
    def setAcceleration(self, accel_mmss):
        """Changes the robot acceleration (in mm/s2)"""
        varname = FilterName(self.ROBOT_NAME).replace('.', '')
        self.addline('    %s.setSpeed(-1,-1,%s,-1)' % (self.CURRENT_PROGRAM_NAME,str(accel_mmss)) )

    def setSpeedJoints(self, speed_degs):
        """Changes the robot joint speed (in deg/s)"""
        varname = FilterName(self.ROBOT_NAME).replace('.', '')
        self.addline('    %s.setSpeed(-1,%s,-1,-1)' % (self.CURRENT_PROGRAM_NAME,str(speed_degs)) )
    
    def setAccelerationJoints(self, accel_degss):
        """Changes the robot joint acceleration (in deg/s2)"""
        varname = FilterName(self.ROBOT_NAME).replace('.', '')
        self.addline('    %s.setSpeed(-1,-1,-1,%s)' % (self.CURRENT_PROGRAM_NAME,str(accel_degss)) )

    def setZoneData(self, zone_mm):
        """Changes the rounding radius (aka CNT, APO or zone data) to make the movement smoother"""
        self.addline('    #Set Zone data (rounding) %s' % str(zone_mm))
        self.addline('    %s.setRounding(%.3f)' % (self.CURRENT_PROGRAM_NAME,zone_mm) )

    def setDO(self, io_var, io_value):
        """Sets a variable (digital output) to a given value"""
        if type(io_var) != str:  # set default variable name if io_var is a number
            io_var = '%s' % str(io_var)
        if type(io_value) != str: # set default variable value if io_value is a number
            if io_value > 0:
                io_value = '1'
            else:
                io_value = '0'

        # at this point, io_var and io_value must be string values
        self.addline('    #Set DO %s %s' % (io_var, io_value))
        self.addline('    %s.setDO(%s,%s)' % (self.CURRENT_PROGRAM_NAME,io_var, io_value))

    def setAO(self, io_var, io_value):
        """Set an Analog Output"""
        self.setDO(io_var, io_value)
        
    def waitDI(self, io_var, io_value, timeout_ms=-1):
        """Waits for a variable (digital input) io_var to attain a given value io_value. Optionally, a timeout can be provided."""
        if type(io_var) != str:  # set default variable name if io_var is a number
            io_var = '%s' % str(io_var)
        if type(io_value) != str: # set default variable value if io_value is a number
            if io_value > 0:
                io_value = '1'
            else:
                io_value = '0'

        # at this point, io_var and io_value must be string values
        if timeout_ms < 0:
            self.addline('    #waitDI %s %s' % (io_var, io_value))
            self.addline('    %s.waitDI(%s,%s)' % (self.CURRENT_PROGRAM_NAME,io_var, io_value))
        else:
            self.addline('    #Wait DI %s %s %.1f' % (io_var, io_value, timeout_ms))
            self.addline('    %s.waitDI(%s,%s,%.1f)' % (self.CURRENT_PROGRAM_NAME,io_var, io_value, timeout_ms))
        
    def RunCode(self, code, is_function_call = False):
        """Adds code or a function call"""
        if is_function_call:
            prognamesafe = FilterName(code).replace('.', '')
            code = code.replace(' ','_')
            self.addline("    " + prognamesafe + '()')
            #Add a call to this function in the main
            if self.POST_CODEGEN_MODE == 3:
                self.addline('    %s = RDK.Item(\'%s\',ITEM_TYPE_PROGRAM)' % (self.MAIN_PROGRAM_NAME,self.MAIN_PROGRAM_NAME))    
                self.addline('    %s.RunInstruction(\'%s\',INSTRUCTION_CALL_PROGRAM)' % (self.MAIN_PROGRAM_NAME,prognamesafe) )
        else:
            self.addline(code)
        
    def RunMessage(self, message, iscomment = False):
        """Display a message in the robot controller screen (teach pendant)"""
        if iscomment:
            self.addline('    #' + message)
        else:
            self.addline('    RDK.ShowMessage(\'%s\',True)' % message)
        
# ------------------ private ----------------------                
    def addline(self, newline):
        """Add a program line"""
        self.PROG = self.PROG + newline + '\n'
        
    def addlog(self, newline):
        """Add a log message"""
        self.LOG = self.LOG + newline + '\n'

# -------------------------------------------------
# ------------ For testing purposes ---------------   
def Pose(xyzrpw):
    [x,y,z,r,p,w] = xyzrpw
    a = r*math.pi/180
    b = p*math.pi/180
    c = w*math.pi/180
    ca = math.cos(a)
    sa = math.sin(a)
    cb = math.cos(b)
    sb = math.sin(b)
    cc = math.cos(c)
    sc = math.sin(c)
    return Mat([[cb*ca, ca*sc*sb - cc*sa, sc*sa + cc*ca*sb, x],[cb*sa, cc*ca + sc*sb*sa, cc*sb*sa - ca*sc, y],[-sb, cb*sc, cc*cb, z],[0,0,0,1]])

def test_post():
    """Test the post with a basic program"""

    def p(xyzrpw):
        x,y,z,r,p,w = xyzrpw
        a = r*math.pi/180.0
        b = p*math.pi/180.0
        c = w*math.pi/180.0
        ca = math.cos(a)
        sa = math.sin(a)
        cb = math.cos(b)
        sb = math.sin(b)
        cc = math.cos(c)
        sc = math.sin(c)
        return Mat([[cb*ca,ca*sc*sb-cc*sa,sc*sa+cc*ca*sb,x],[cb*sa,cc*ca+sc*sb*sa,cc*sb*sa-ca*sc,y],[-sb,cb*sc,cc*cb,z],[0.0,0.0,0.0,1.0]])
        
    robot = RobotPost(r"""Quine""",r"""ABB IRB 120-3/0.6""",6, axes_type=['R','R','R','R','R','R'], 
    ip_com=r"""192.168.125.1""")

    robot.ProgStart(r"""Prog1""")
    robot.RunMessage(r"""Program generated by RoboDK v4.2.3 for ABB IRB 120-3/0.6 on 08/05/2020 15:54:54""", True)
    robot.RunMessage(r"""Using nominal kinematics.""", True)
    robot.setFrame(p([0.000000,0.000000,0.000000,0.000000,0.000000,0.000000]),-1,r"""ABB IRB 120-3/0.6 Base""")
    robot.setAccelerationJoints(800.000)
    robot.setSpeedJoints(500.000)
    robot.setAcceleration(3000.000)
    robot.setSpeed(500.000)
    robot.MoveJ(p([374.000000,-0.000000,610.000000,-0.000000,90.000000,0.000000]),[-0.000000,-0.836761,4.599793,-0.000000,-3.763032,0.000000],[0.0,0.0,1.0])
    robot.MoveL(p([374.000000,174.400321,610.000000,0.000000,90.000000,0.000000]),[30.005768,9.246934,-6.136218,84.631745,-30.151638,-83.797873],[0.0,0.0,1.0])
    robot.MoveL(p([374.000000,-201.108593,610.000000,0.000000,90.000000,0.000000]),[-33.660539,12.400929,-9.814293,-86.122958,-33.748102,85.340395],[0.0,0.0,1.0])
    robot.MoveJ(p([374.000000,-0.000000,610.000000,-0.000000,90.000000,0.000000]),[-0.000000,-0.836761,4.599793,-0.000000,-3.763032,0.000000],[0.0,0.0,1.0])
    robot.setTool(p([0.000000,0.000000,200.000000,0.000000,0.000000,0.000000]),-1,r"""Paint gun""")
    robot.MoveC(p([374.000000,-0.000000,610.000000,-0.000000,90.000000,0.000000]),[-0.000000,-0.836761,4.599793,-0.000000,-3.763032,0.000000],p([374.000000,-201.108593,610.000000,0.000000,90.000000,0.000000]),[-33.660539,12.400929,-9.814293,-86.122958,-33.748102,85.340395],[0.0,0.0,1.0],[0.0,0.0,1.0])
    robot.setZoneData(10.000)
    robot.setDO(5,1)
    robot.setAO(5,1)
    robot.waitDI(5,1,5000)
    robot.waitDI(5,1,-1)
    robot.RunMessage(r"""Display message""")
    robot.ProgFinish(r"""ajkslfh""")
    print(robot.PROG)
    if len(robot.LOG) > 0:
        mbox('Program generation LOG:\n\n' + robot.LOG)
    input("Press Enter to close...")
    return
    # robot.ProgSave(".","Program",True)
    print(robot.PROG)
    if len(robot.LOG) > 0:
        mbox('Program generation LOG:\n\n' + robot.LOG)

    input("Press Enter to close...")

if __name__ == "__main__":
    """Function to call when the module is executed by itself: test"""
    test_post()
