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
warned = False


def getLocalSurfacers():
    #Should already be checked but just in case
    if fileFormatCheck("surfacing"):
        publishSurfaces()

def publishSurfaces():
    #get scene objects
    theNodes = cmds.ls(dag = True, s = True, o = True)
    list = json.loads('{"geo":"shader"}') 
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
    
def newVersFormat(objName):
    print(objName)
    print(objName.split('.')[1].split('v')[1])
    return str(int(objName.split('.')[1].split('v')[1])+1)
            
    

def checkPrevFileAndSave(list):
    #TO DO: need to create a check for folders/create (material, source, textures)
    file_list=os.listdir(pubFolderpath+'material/')
    #Check for Previous JSON files
    for file in file_list:
        if "json" in file:
            fileName = file
    #msg for created files
    msg = ""
    if 'fileName' in locals():
        #Check if updates have been made
        if sameJson(pubFolderpath+'material/'+fileName, list) == False:
            #MAYA SHADER
            file_list=os.listdir(pubFolderpath+'material/')
            #Check for existing file
            for file in file_list:
                if "shader." in file:
                    shaderFile = file
            shaderName = objname+"_shader.v"+newVersFormat(shaderFile)
            cmds.file(rename = pubFolderpath+'material/'+shaderName)
            cmds.file(s=True,f=True)
            msg += "\nVersion "+newVersFormat(shaderFile)+" Shader file made."
            
            #MAYA SOURCE
            file_list=os.listdir(pubFolderpath+'source/')
            #Check for existing maya surface file
            for file in file_list:
                if "surface" in file:
                    surfaceFile = file
            surfaceName = objname+"_surface.v"+newVersFormat(surfaceFile)
            cmds.file(rename = pubFolderpath+'source/'+surfaceName)
            cmds.file(s=True,f=True)
            #ALSO WIP MAYA FILE
            cmds.file(rename = folderpath+objname+"_surface.v"+newVersFormat(filepath))
            cmds.file(s=True,f=True)
            msg+="\nVersion "+newVersFormat(surfaceFile)+" Surface maya file made."
            
            #JSON
            version = int(fileName.split('_')[2].split('.')[0].split('v')[1])
            with open(pubFolderpath+'material/'+objname+'_shaderList'+'_v'+str(version+1)+'.json', "w") as outfile:
                json.dump(list, outfile)
            msg+="\nVersion "+str(version+1)+" Geo/Shade Json file made."
            
            #Success Message
            cmds.confirmDialog( title='Success', message=msg)
        else:
            cmds.confirmDialog( title='Warning', message="No changes to shaders made.")
    else:
        #FIRST MAYA SHADER
        shaderName = objname+"_shader.v001.mb"
        cmds.file(rename = pubFolderpath+'material/'+shaderName)
        cmds.file(s=True,f=True)
        msg+="\nFirst version shader published file made."

        #FIRST MAYA SOURCE FILE
        surfaceName = objname+"_surface.v001.mb"
        cmds.file(rename = pubFolderpath+'source/'+surfaceName)
        cmds.file(s=True,f=True)
        #ALSO WIP MAYA FILE
        cmds.file(rename = folderpath+objname+"_surface.v"+newVersFormat(filepath))
        cmds.file(s=True,f=True)
        msg+="\nFirst version source maya published file made."
        
        #FIRST JSON
        with open(pubFolderpath+'material/'+objname+'_shaderList_v001.json', "w") as outfile:
            json.dump(list, outfile)
        msg+="\nFirst version of shader json List published file made."
        cmds.confirmDialog( title='Success', message=msg)

def sameJson(oldfile, new):
    old = json.load(open(oldfile))
    if old == new:
        return True
    else:
        return False

def getSelShaderPath():
    #get selected
    selected = cmds.ls(sl=True,long=True)
    if not selected==[]:
        #get model ref path of selected
        refFolderpath = cmds.referenceQuery(selected[0][1:], filename = True)
        #get surfacing path of selected
        return refFolderpath.split('model')[0]+'surfacing/material/'
    else:
        cmds.confirmDialog( title='Warning', message="Nothing selected. Please select object.")
        return ""
    

def setSurfaces(version):
    if fileFormatCheck("light"):
        #get surface model path
        shaderFolderpath = getSelShaderPath()
        #Some paths don't work
        #if shaderFolderpath 
        if shaderFolderpath != "":
            if version == "latest":
                file_list=os.listdir(shaderFolderpath)
                jsonArray = []
                #check that path has material folder/exists
                for file in file_list:
                    if "json" in file:
                        jsonArray.append(file)
                #Check if this object's JSON shaderlist exists
                if jsonArray != []:
                    jsonFile = jsonArray[-1]
                    #Show latest vers in textbox
                    cmds.textField("Version", edit=True, tx=jsonFile)
                    list = json.load(open(shaderFolderpath+jsonFile))
                else:
                    list = ""
            elif version == "older":
                #get JSON input vers from textfield
                jsonFile = "armchair01_shaderList_v3.json"
                #get surface model path
                shaderFolderpath = getSelShaderPath()
                print(shaderFolderpath+jsonFile)
                list = json.load(open(shaderFolderpath+jsonFile))
            #Check for ShaderlList
            if list != "":
                #get specific files that match shaderlist
                version = jsonFile.split('_')[2].split('.')[0].split('v')[1]
                #shader file
                file_list=os.listdir(shaderFolderpath)
                shaderFile = ''
                for file in file_list:
                    if "shader." in file:
                        if version in file:
                            shaderPath = shaderFolderpath+file
                #source file (USEFUL???)
                sourceFile = ''
                sourceFolderpath = '/'.join(shaderFolderpath.split('/')[:-2])+'/source/'
                file_list=os.listdir(sourceFolderpath)
                for file in file_list:
                    if "surface" in file:
                        if version in file:
                            sourcePath = sourceFolderpath+file
                #Import shaders
                cmds.file(shaderPath, i=True, mergeNamespacesOnClash=True)
                #Loop through List and apply shaders
                for geo, shader in list.items():
                    print(geo)
                    #cmds.select(geo)
                    print(shader)
                    selected = cmds.ls(sl=True,long=True)
                    selected.append(shader)
                    #unShaded.append(objects[i])
                    #where geo == this file's geo
                    #where shader == shaderSources' shader
                    #assign
            else:
                cmds.confirmDialog( title='Warning', message="No shaderlist exists.")            
    else:
        cmds.confirmDialog( title='Warning', message="This is not a lighting file. Please open a lighting file to assign surfacers.")
    

def fileFormatCheck(type):
    global warned
    #get file directory and folder
    filepath = cmds.file(q=True, sn=True)
    fileType = filepath.split('/')[-2]
    if 'wip' in filepath:
        if fileType == type:
            return True
        else:
            return False
    elif warned == False:
        warned = True
        cmds.confirmDialog( title='Warning', message="Currently not working in wip directory. Please change to wip.")
        return False
    else:
        return False
        
def assignTool():
    if cmds.window('assignTool', exists = True):
        cmds.deleteUI('assignTool', window = True)
        
    cmds.window('assignTool', title='assignTool', resizeToFitChildren=True)
    
    with LayoutManager(cmds.columnLayout(adj=True, rowSpacing=5)) as col:
        isSurfacing = fileFormatCheck("surfacing") 
        cmds.separator(h=20)
        cmds.text('Surfacing', en = isSurfacing)
        cmds.button(label = 'Publish Shaders', command = 'getLocalSurfacers()', en = isSurfacing)
        SurfaceText = cmds.textField(en=False, tx="" )
        cmds.separator(h=20)
        
        isLighting = fileFormatCheck("light") 
        cmds.text('Lighting', en = isLighting)
        cmds.button(l = 'Set Selected Latest Shader', command = 'setSurfaces("latest")', en = isLighting)
        shaderList = cmds.textField('Version', en = isLighting)
        cmds.button(l = 'Set Selected Version Shader', command = 'setSurfaces("older")', en = isLighting)
        cmds.separator(h=20)
        if warned == False:
            cmds.showWindow('assignTool')

assignTool()
