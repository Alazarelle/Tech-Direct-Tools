import maya.cmds as cmds
from maya.common.ui import LayoutManager
import os.path
import json

#Location data
filepath = cmds.file(q=True, sn=True)
filename = filepath.split('/')[-1]
objname = filename.split('_')[0]
folderpath = '/'.join(filepath.split('/')[:-1])+'/'
location = filepath.split('/')[-6]
pubFolderpath = folderpath.split(location)[0]+'publish'+folderpath.split(location)[1]


def getLocalSurfacers():
    #Should already be checked but just in case
    if fileFormatCheck("surfacing"):
        publishSurfaces()
    else:
        print("This is not a surfacing file. Please open a surfacing file to publish surfacers.")

def publishSurfaces():
    #get scene objects
    theNodes = cmds.ls(dag = True, s = True, o = True)
    list = {}
    #Go through scene
    for shade in theNodes:
        #Geometry
        geo = shade.split('Shape')[0]
        shadeEng = cmds.listConnections(shade , type = 'shadingEngine')
        #don't get no shader objects
        if shadeEng is None:
            #ignore (TO DO: Is there a better ay to do the reverse of this?)
            print("ignoring "+geo)
        else:
            material = cmds.ls(cmds.listConnections(shadeEng), materials = True)
            val={str(geo):str(material[0])}
            list.update(val)
    checkPrevFileAndSave(list)

def checkPrevFileAndSave(list):
    print("")
    #TO DO: need to create a check for folders/create (material, source, textures)
    file_list=os.listdir(pubFolderpath+'material/')
   #Check for Previous JSON files
    for file in file_list:
        if "json" in file:
            fileName = file
    if 'fileName' in locals():
        #Check if updates have been made
        if sameJson(pubFolderpath+'material/'+fileName, list) == False:  
            #MAYA SHADER
            file_list=os.listdir(pubFolderpath+'material/')
            #Check for existing file
            for file in file_list:
                if "shader." in file:
                    shaderFile = file
                    shaderVers = int(shaderFile.split('.')[1].split('v')[1])
            shaderName = objname+"_shader.v"+str(shaderVers+1)
            cmds.file(rename = pubFolderpath+'material/'+shaderName)
            cmds.file(s=True,f=True)
            print("Version "+str(shaderVers+1)+" Shader file made.")
            
            #MAYA SOURCE
            file_list=os.listdir(pubFolderpath+'source/')
            #Check for existing maya surface file
            for file in file_list:
                if "surface" in file:
                    surfaceFile = file
                    surfaceVers = int(shaderFile.split('.')[1].split('v')[1])
            surfaceName = objname+"_surface.v"+str(surfaceVers+1)
            cmds.file(rename = pubFolderpath+'source/'+surfaceName)
            cmds.file(s=True,f=True)
            print("Version "+str(surfaceVers+1)+" Surface maya file made.")
            
            #JSON
            version = int(fileName.split('_')[2].split('.')[0].split('v')[1])
            list.update({str(surfaceName):str(shaderName)})
            with open(pubFolderpath+'material/'+objname+'_shaderList'+'_v'+str(version+1)+'.json', "w") as outfile:
                json.dump(list, outfile)
            print("Version "+str(version+1)+" Geo/Shade Json file made.")
            
            #save published file
            #newShaderfilepath = pubFolderpath+'material/'+filename.split('surface')[0]+'shader'+newfilepath.split('surface')[1]
            #cmds.file(rename = newShaderfilepath)
            #cmds.file(s=True, f=True)
            #reopen wip surface file
            #cmds.file(newfilepath+".mb", open=True )
            #SurfaceText = cmds.textField("surfaceText", tx="No changes made to shaders.")
            #save published file
            #newShaderfilepath = pubFolderpath+'material/'+filename.split('surface')[0]+'shader'+newfilepath.split('surface')[1]
            #cmds.file(rename = newShaderfilepath)
            #cmds.file(s=True, f=True)
            #reopen wip surface file
            #cmds.file(newfilepath+".mb", open=True )
            #print("First Geo/Shade Json file made, new wip and updated published maya files made.")
            #need to update window- assignTool()
        else:
            print("No changes to shaders made.")
    else:
        #FIRST MAYA SHADER
        shaderName = objname+"_shader.v001.mb"
        cmds.file(rename = pubFolderpath+'material/'+shaderName)
        cmds.file(s=True,f=True)
        print("First version shader published file made.")

        #FIRST MAYA SOURCE FILE
        surfaceName = objname+"_surface.v001.mb"
        cmds.file(rename = pubFolderpath+'source/'+surfaceName)
        cmds.file(s=True,f=True)
        print("First version surface published file made.")
        
        #FIRST JSON
        list.update({str(surfaceName):str(shaderName)})
        with open(pubFolderpath+'material/'+objname+'_shaderList_v001.json', "w") as outfile:
            json.dump(list, outfile)
        print("First version of shader json List published file made.")
    print("")


def sameJson(oldfile, new):
    old = json.load(open(oldfile))
    if old == new:
        return True
    else:
        return False

def getPubSurfacers(state):
    if fileFormatCheck("light"):
        if state == "load":
            loadSurfaces()
        elif state == "set":
            setSurfaces()
    else:
        print("This is not a lighting file. Please open a lighting file to assign surfacers.")


def loadSurfaces():
    #get selected
    selected = cmds.ls(sl=True,long=True)
    if not selected==[]:
        #get ref path of selected
        refFolderpath = cmds.referenceQuery(selected[0][1:], filename = True)
        #get surfacing path of selected
        surfaceFolderpath = refFolderpath.split('model')[0]+'surfacing/material/'
        #get json files
        file_list=os.listdir(surfaceFolderpath)
        jsonArray = []
        for file in file_list:
            if "json" in file:
                jsonArray.append(file)
        cmds.textField("Version", edit=True, tx=jsonArray[-1])


    else:
        print("Nothing selected. Please select object.")

def setSurfaces():
    list = json.load(open(surfaceFolderpath+"val"))
    #get specific shader maya file
    for geo, shader in list.items():
        shaderSource = shader
    print(shaderSource)
    #Get shaders from file
    #Loop through List and apply shaders
    for geo, shader in list.items():
        #where geo == this file's geo
        #where shader == shaderSources' shader
        #assign
    

def fileFormatCheck(type):
    #get file directory and folder
    fileType = filepath.split('/')[-2]    
    if location == "wip":
        if fileType == type:
            return True
        else:
            return False
    else:
        if location == "publish":
            print("Currently working in publish directory. Please change to wip.")
        else:
            print("Currently not working in wip directory. Please change to wip.")
        return False
        
def assignTool():
    #close old windows
    if cmds.window('assignTool', exists = True):
        cmds.deleteUI('assignTool', window = True)
        
    cmds.window('assignTool', title='assignTool', resizeToFitChildren=True)
    
    with LayoutManager(cmds.columnLayout(adj=True, rowSpacing=5)) as col:
        isSurfacing = fileFormatCheck("surfacing") 
        cmds.separator(h=20)
        cmds.text('Surfacing', en = isSurfacing)
        cmds.button(label = 'Publish Shaders', command = 'getLocalSurfacers()', en = isSurfacing)
        #cmds.text(label='')
        SurfaceText = cmds.textField(en=False, tx="" )
        cmds.separator(h=20)
        
        isLighting = fileFormatCheck("light") 
        cmds.text('Lighting', en = isLighting)
        cmds.button(l = 'Get Selected Latest Shader', command = 'getPubSurfacers("load")', en = isLighting)
        #cmds.textFieldGrp(label='Version:', text="1", en = isLighting)
        cmds.textField('Version', text="", en = isLighting)
        cmds.button(l = 'Assign Shaders', command = 'getPubSurfacers("set")', en = isLighting)
        #cmds.text('')
        cmds.separator(h=20)
        #cmds.text("...")
        cmds.showWindow('assignTool')

assignTool()
