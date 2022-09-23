import maya.cmds as cmds
from maya.common.ui import LayoutManager


def getSurfacers():
    cameraName = cmds.camera(horizontalFilmAperture=1.247, verticalFilmAperture=0.702, farClipPlane=100000)
    #In Surfacing Maya File (WIP Folder):
    #Upon clicking publish shaders button:
    #Get list of assigned shaders in scene. (In either order)
    #Get list of associated via parent objects in scene. (In either order)
    #Loop list to create Json list of each geometry object name and shader name.
    #Save Json file to publish/surfacing folder with +1 to version name

def setSurfacers():
    cameraName = cmds.camera(horizontalFilmAperture=1.247, verticalFilmAperture=0.702, farClipPlane=100000)
    #In Lighting Maya File (WIP Folder):
    #Upon clicking load shaders button:
    #Get list of geometry objects in the scene.
    #Get Json list (from publish folder) and get list of the associated shaders
    #Loop through scene geo list and get the associated shader (ref from published)
    #Assign associated shader to the object.
    #Optional: select latest button (does above) or show list of all vers for each object (within the same folder and of the same name) and select one to assign


def fileFormat(type):
    if type == "surfacing":
        return True
    elif type == "lighting":
        return False

def assignTool():
    #close old windows
    if cmds.window('assignTool', exists = True):
        cmds.deleteUI('assignTool', window = True)
        
    cmds.window('assignTool', title='assignTool', resizeToFitChildren=True)
    
    with LayoutManager(cmds.columnLayout(adj=True, rowSpacing=5)) as col:
        isSurfacing = fileFormat("surfacing") 
        cmds.separator(h=20)
        cmds.text('Surfacing', en = isSurfacing)
        cmds.button(label = 'Publish Shaders', command = 'getSurfacers()', en = isSurfacing)
        #cmds.text('', id = 'publishError')
        cmds.separator(h=20)
        
        isLighting = fileFormat("lighting") 
        cmds.text('Lighting', en = isLighting)
        cmds.textFieldGrp(label='Version:', text="1", en = isLighting)
        cmds.button(label = 'Assign Shaders', command = 'setSurfacers()', en = isLighting)
        #cmds.text('')
        cmds.separator(h=20)
    
        cmds.showWindow('assignTool')

assignTool()
