import maya.cmds as cmds
from maya.common.ui import LayoutManager
import os.path
import json

#Location data
filepath = cmds.file(q=True, sn=True)
filename = filepath.split('/')[-1]
objname = filename.split('_')[0]
folderpath = '/'.join(filepath.split('/')[:-1])+'/'
wipLocation = filepath.split('/')[-6]
pubFolderpath = folderpath.split(wipLocation)[0]+'publish'+folderpath.split(wipLocation)[1]
global warned
warned = False

#Multi-use functions
def newVersFormat(obj, type):
    if obj == "": return "001"
    else:
        if (type == 'json'): vers = int(obj.split('_')[2].split('.')[0].split('v')[1])+1
        else: vers = int(obj.split('.')[1].split('v')[1])+1
    if vers < 10: return "00" + str(vers)
    elif vers < 100: return "0" + str(vers)
    return str(vers)

def sameJson(oldfile, new):
    old = json.load(open(oldfile))
    if old == new: return True
    else: return False

def fileFormatCheck(type):
    warned = False
    #get file directory and folder
    filepath = cmds.file(q=True, sn=True)
    fileType = filepath.split('/')[-2]
    if 'wip' in filepath:
        if fileType == type:return True
        else: return False
    elif warned == False:
        warned = True
        cmds.confirmDialog( title='Warning', message="Currently not working in wip directory. Please change to wip.")
        return False
    else: return False
              
def getSelShaderPath():
    #get selected
    selected = cmds.ls(sl=True,long=True)
    if not selected==[]:return cmds.referenceQuery(selected[0][1:], filename = True).split('model')[0]+'surfacing/material/'
    else:
        cmds.confirmDialog( title='Warning', message="Nothing selected. Please select object.")
        return ""

def clearList():
    menuItems = cmds.optionMenu('shaderVersList', q=True, itemListLong=True)
    if menuItems: cmds.deleteUI(menuItems)

#Methods
def publishSurfaces():
    if fileFormatCheck("surfacing"):
        #get scene objects
        theNodes = cmds.ls(dag = True, s = True, o = True)
        list = {} 
        #Go through scene
        for shade in theNodes:
            #Geometry
            geo = shade.split('Shape')[0]
            shadeEng = cmds.listConnections(shade , type = 'shadingEngine')
            #don't get no shader objects
            if shadeEng is not None:
                material = cmds.ls(cmds.listConnections(shadeEng), materials = True)
                val={str(geo):str(material[0])}
                list.update(val)
        checkPrevFileAndSave(list)
    else: cmds.confirmDialog( title='Warning', message="This is not a surfacing file. Please open a surfacing file to publish surfacers.")

def checkPrevFileAndSave(list):
    #path checks (create if they don't exist
    if (os.path.exists(pubFolderpath+'material/') == False): os.makedirs(pubFolderpath+'material/')
    if (os.path.exists(pubFolderpath+'source/') == False): os.makedirs(pubFolderpath+'source/')
    if (os.path.exists(pubFolderpath+'textures/') == False): os.makedirs(pubFolderpath+'textures/') 
    file_list=os.listdir(pubFolderpath+'material/')
    #Check for Previous JSON files
    for file in file_list:
        if "json" in file: fileName = file
    #msg for created files
    msg = ""
    #If first time creating
    if 'fileName' not in locals(): fileName = shaderFile = surfaceFile = ""
    #Create files + check for ShaderList updates
    if (fileName == "" or sameJson(pubFolderpath+'material/'+fileName, list) == False):

        #MAYA SHADER
        file_list=os.listdir(pubFolderpath+'material/')
        #Check for existing file
        for file in file_list:
            if "shader." in file: shaderFile = file
        shaderName = objname+"_shader.v"+newVersFormat(shaderFile, "shader")
        #select shaders to be exported
        shaders = []
        for geo, shader in list.items():
            shaders.append(shader)
        cmds.select(shaders)
        cmds.file(rename = pubFolderpath+'material/'+shaderName)
        cmds.file(f=True, op= "v=0;", typ = "mayaBinary", pr=True, es=True)
        msg += "\nVersion "+newVersFormat(shaderFile, "shader")+" Shader file made."
        
        #MAYA SOURCE
        file_list=os.listdir(pubFolderpath+'source/')
        #Check for existing maya surface file
        for file in file_list:
            if "surface" in file: surfaceFile = file
        surfaceName = objname+"_surface.v"+newVersFormat(surfaceFile, "surface")
        cmds.file(rename = pubFolderpath+'source/'+surfaceName)
        cmds.file(s=True,f=True)
        #ALSO WIP MAYA FILE
        cmds.file(rename = folderpath+objname+"_surface.v"+newVersFormat(filepath, "surface"))
        cmds.file(s=True,f=True)
        msg+="\nVersion "+newVersFormat(surfaceFile, "surface")+" Surface maya file made."
        
        #JSON
        with open(pubFolderpath+'material/'+objname+'_shaderList_v'+newVersFormat(fileName, "json")+'.json', "w") as outfile:
            json.dump(list, outfile)
        msg+="\nVersion "+newVersFormat(fileName, "json")+" Geo/Shade Json file made."
        #Success Message
        cmds.confirmDialog( title='Success', message=msg)
    else:
        cmds.confirmDialog( title='Warning', message="No changes to shaders made.")
     
def GetSurfaceList():
    clearList()
    shaderList = []
    jsonArray = []
    shaderFolderpath = getSelShaderPath()
    if shaderFolderpath != "":
        if os.path.exists(shaderFolderpath):
            file_list=os.listdir(shaderFolderpath)
            #check that path has material folder/exists
            for file in file_list:
                if "json" in file: jsonArray.append(file)
        if jsonArray == []: cmds.confirmDialog( title='Warning', message="No shaderlist exists.")
        else: 
            for vers in jsonArray:
                shaderList = cmds.menuItem(p='shaderVersList', label = vers)

def setSurfaces():
    if fileFormatCheck("light"):
        warned = False
        #get Shaderlist
        shaderVers = cmds.optionMenu('shaderVersList', q=True, v=True)
        if shaderVers is None: cmds.confirmDialog( title='Warning', message="No Object and Shaders selected.")
        else:
            theNodes = cmds.ls(dag = True, s = True, o = True)
            sceneGeo = ""
            #Go through scene
            for shade in theNodes:
                #Geometry
                geo = shade.split('Shape')[0]
                if "mRef" in geo: sceneGeo = geo.split(':')[0]+":"
            #get path
            shaderFolderpath = getSelShaderPath()
            if os.path.exists(shaderFolderpath+shaderVers):
                shaderList = json.load(open(shaderFolderpath+shaderVers))
                #get and import associated shader file
                file_list=os.listdir(shaderFolderpath)
                obj = shaderVers.split('_')[0]
                vers = shaderVers.split('v')[-1].split('.')[0]
                namespace = shaderVers.split('.')[0]
                for file in file_list:
                    if "shader." in file:
                        if vers in file: shaderFile = file
                importedShaders = cmds.file(shaderFolderpath+shaderFile, i=True, mergeNamespacesOnClash=True, namespace=namespace)
                for geo, shader in shaderList.items():
                    #Select proper Geo and assign shader
                    if cmds.ls(sceneGeo+geo) == [] and warned == False:
                        warned = True
                        cmds.confirmDialog( title='Warning', message="This object's model and/or names are not set up correctly for shaders.")
                    else:
                        cmds.select(cmds.ls(sceneGeo+geo)[0])
                        cmds.hyperShade(assign = (namespace+":"+shader))
            else: cmds.confirmDialog( title='Warning', message="The shaderList is not applicable to selected. Have you selected a different model?")
    else: cmds.confirmDialog( title='Warning', message="This is not a lighting file. Please open a lighting file to assign surfacers.")

#Window   
def assignTool():
    if cmds.window('assignTool', exists = True): cmds.deleteUI('assignTool', window = True)
        
    cmds.window('assignTool', title='Shader Tool', widthHeight = (250, 300), sizeable = False, resizeToFitChildren = True)
    with LayoutManager(cmds.columnLayout(adj=True, rowSpacing=5)) as col:
        cmds.separator(h=20)
        cmds.text("SHADER ASSIGNER", font="boldLabelFont")
        #Surfacing
        isSurfacing = fileFormatCheck("surfacing")
        cmds.separator(h=20)
        cmds.text('Surfacing', font="boldLabelFont", en = isSurfacing)
        if isSurfacing: cmds.text(objname, font='smallObliqueLabelFont', en = isSurfacing)
        cmds.button(label = 'Publish Shaders', command = 'publishSurfaces()', en = isSurfacing)
        cmds.separator(h=20)
        #Lighting
        isLighting = fileFormatCheck("light") 
        cmds.text('Lighting', en = isLighting, font="boldLabelFont")
        if isLighting: cmds.text(filename, font='smallObliqueLabelFont', en = isLighting)
        cmds.button(l = 'Get Selected Shaders', command = 'GetSurfaceList()', en = isLighting)
        cmds.optionMenu('shaderVersList', en = isLighting)
        shaderList = ""
        cmds.button(l = 'Assign Shader Version to Selected', command = 'setSurfaces()', en = isLighting)
        cmds.separator(h=20)
        if warned == False: cmds.showWindow('assignTool')

assignTool()
