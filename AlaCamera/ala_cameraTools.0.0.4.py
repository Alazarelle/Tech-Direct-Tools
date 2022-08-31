 # ala_cameraTools.0.03.py
# This tool creates a camera based on a real world camera, and lets user set Arri Master Prime focal lengths.

import maya.cmds as cmds

# creates an AlexaLF camera and sets the film back. Sets the Far Clip PLane to 10,000. Also setting the render settings to HD.
def createCamera():
    cameraName = cmds.camera(position = [-20,200,-590], rotation = [-8,-160,0], horizontalFilmAperture=1.247, verticalFilmAperture=0.702, farClipPlane=100000)
    setResolutionWidth = cmds.setAttr('defaultResolution.width', 1920)
    setResolutionHeight = cmds.setAttr('defaultResolution.height', 1080)
    setDeviceAspectRatio = cmds.setAttr('defaultResolution.deviceAspectRatio', 1.778)
    setScale = cmds.setAttr(cameraName[0]+".scale", 20,20,20,)
    print("Camera created")

# Sets the camera Aperature made by the pipeline to match an AlexaLF camera. And sets the scene Render Settings to HD.
def alexaCamera():
    for each_cam_tf in cmds.ls(sl=True):
        cam_shp = cmds.listRelatives(each_cam_tf,type="camera")
        if cam_shp:
            cmds.setAttr(cam_shp[0]+".horizontalFilmAperture", 1.247)
            cmds.setAttr(cam_shp[0]+".verticalFilmAperture", 0.702)
            cmds.setAttr(cam_shp[0]+".farClipPlane", 100000)
    
    setResolutionWidth = cmds.setAttr('defaultResolution.width', 1920)
    setResolutionHeight = cmds.setAttr('defaultResolution.height', 1080)
    setDeviceAspectRatio = cmds.setAttr('defaultResolution.deviceAspectRatio', 1.778)
    print("Every Camera set to match AlexaLf Camera settings and Render settings to HD.")

def getFocalLength():
    print('Enter focal length:')
    num = input()
    focalLength(int(num))
    
def focalLength(num):
    #loop over all cameras that are selected (transform node)
    for each_cam_tf in cmds.ls(sl=True):
        #find the shape node
        cam_shp = cmds.listRelatives(each_cam_tf,type="camera")
        #only set attr if a camera shape was found 
        if cam_shp:
        #set focal length
            cmds.setAttr(cam_shp[0]+".fl", num)
            #send msg
            sendLengthMsg(num)

def sendLengthMsg(length):
#Shows message of changes
    print("Focal length of selected camera is now "+str(length)+"mm.")

def viewThroughCamera():
    for each_cam_tf in cmds.ls(sl=True):
        cam_shp = cmds.listRelatives(each_cam_tf,type="camera")
        if cam_shp:
            cmds.lookThru(cam_shp[0])

def viewThroughCameraExit():
    cmds.lookThru("persp")

def setDepthOfField():
    for each_cam_tf in cmds.ls(sl=True):
        cam_shp = cmds.listRelatives(each_cam_tf,type="camera")
        if cam_shp:
            isOn = cmds.getAttr(cam_shp[0]+".dof")
            if isOn:
                cmds.setAttr(cam_shp[0]+".dof", 0)
                print("Depth of Field of selected camera is now off.")
                editDepthOfField(each_cam_tf, "off")
            else:
                cmds.setAttr(cam_shp[0]+".dof", 1)
                print("Depth of Field of selected camera is now on.")
                editDepthOfField(each_cam_tf, "on")

def editDepthOfField(camera, val):
    if val == "on":
        # get camera pos
        camPosX = cmds.getAttr(camera+'.translateX')
        camPosY = cmds.getAttr(camera+'.translateY')
        camPosZ = cmds.getAttr(camera+'.translateZ')
        #create distance as camera pos and car
        dim = cmds.distanceDimension(sp=(camPosX,camPosY,camPosZ),ep=(-15, 62,-182))
        #sp = cmds.getAttr(dim+'.sp')
        #print(sp)
        # ONLY WORKS FOR 1 CAM
        cmds.rename('locator1', 'cameraPoint')
        cmds.parent('cameraPoint', camera)
        #cmds.parent(sp[0], camera)
        #cmds.select("locator")
        #Connect focus to distance
        cmds.connectAttr(dim+'.distance', camera+'.focusDistance')
        for each_loc_tf in cmds.ls(sl=True):
        loc_shp = cmds.listRelatives(each_loc_tf,type="locator")
        if loc_shp:
            cmds.group(camera,dim, loc_shp[0])
        cmds.select(camera)
    elif val == "off":
        #get cam point
        point =cmds.listRelatives()[1]
        #cmds.delete(point)

def cameraTools():
    if cmds.window('cameraTools', exists = True):
        cmds.deleteUI('cameraTools')
    
    cmds.window('cameraTools', resizeToFitChildren=True)    
    cmds.columnLayout()
    
    cmds.separator(h=10)
    cmds.text('PREVIS:')
    cmds.separator(h=10)
    
    cmds.text('Creates an AlexaLF camera')
    #cmds.text('Set the correct render settings')
    cmds.separator(h=5)
    cmds.button(label = 'Create Camera', command = 'createCamera()')
    
    
    cmds.separator(h=30)
    cmds.text('LAYOUT:')
    cmds.separator(h=10)
    
    cmds.text('Set AlexaLF Settings')
    cmds.separator(h=5)
    cmds.button(label = 'Set all cameras', command = 'alexaCamera()')
    
    cmds.separator(h=10)
    cmds.text('View through selected Camera')
    cmds.separator(h=5)
    cmds.button(label = 'See Camera View', command = 'viewThroughCamera()')
    cmds.separator(h=5)
    cmds.button(label = 'Leave Camera View', command = 'viewThroughCameraExit()')
    
    
    cmds.separator(h=10)
    cmds.text('Sets focal length on selected camera.')
    cmds.separator(h=5)
    cmds.button(label = 'Set Focal Length', command = 'getFocalLength()')
    
    cmds.separator(h=10)
    cmds.text('Set Depth of Field on or off for selected camera.')
    cmds.separator(h=5)
    cmds.button(label = 'Depth Of Field', command = 'setDepthOfField()')
    cmds.separator(h=10)
    
    cmds.showWindow('cameraTools')



cameraTools()
