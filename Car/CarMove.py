import maya.cmds as cmds
import random as rand
from mtoa.core import createStandIn

#create curve
selectCurve = input('Do you wish to use selected curve? y/n: ')
if selectCurve == "y":
    path = cmds.ls(sl=1,sn=True)[0]
    print('Selected path used.')
else:
    path = cmds.curve( p=[(-868, 0, 736), (-325, 0,725), (261, 0, 698), (577, 0, 701), (726, 0, 426), (721, 0, -312), (729, 0, -536), (720, 0, -851)] )
    print('Created path used.')

#multiple cars amount
carAmount = int(input('Enter amounnt of cars to generate: '))
print(carAmount)

#select end keyframe
endFrame = int(input('Speed: '))
print(endFrame)

#set up path
#pathFile = input('Set path for car assets: ')
#print(pathFile)
#if ':\' not in pathFile:
    #pathFile = 'C:\\Users\\alaza\\Documents\\GitHub\\Tech-Direct-Tools\\Car'

#Loop through each car iteration
for car in range(carAmount):
    #create locator
    carLoc = cmds.spaceLocator()
    cmds.scale(100,100,100)
    #create arnold standIn
    standIn = createStandIn()
    standIn = cmds.rename(standIn, 'standIn'+str(car))
    #pair stanIn to locator/car
    cmds.parent(standIn, carLoc)
    #create motion path
    mp = cmds.pathAnimation( carLoc[0], c=path, follow=True)
    #Add offset to every second val
    if (car % 2) != 0:
        child = cmds.listRelatives(carLoc[0])[1]
        print(child)
        cmds.move(0,0,300, standIn, relative=True)
    #disconnect set u value
    cmds.disconnectAttr(mp+'_uValue.output', mp+'.uValue')
    #create Speed Controller
    speedCont = cmds.group( em=True, name='SpeedControllor' )
    cmds.addAttr( longName='speed', defaultValue=0, minValue=0, maxValue=5)
    #connect speed to motion path u val
    cmds.connectAttr(speedCont+'.speed', mp+'.uValue')
    #set key frames start
    num = rand.randint(17,20)
    cmds.currentTime(car*num)
    cmds.setAttr( speedCont+'.speed', 0 )
    cmds.setKeyframe(speedCont+'.speed')
    #set key frame end
    cmds.currentTime(endFrame+(car*num))
    cmds.setAttr( speedCont+'.speed', 5 )
    cmds.setKeyframe(speedCont+'.speed')
    print(str(car) + "*" + str(num) + "=" + str(car*num))
    #import car standin
    assets = ['car02_v001.ass', 'car01_v002.ass', 'car03_v001.ass']
    cmds.setAttr( standIn+'.dso','C:\\Users\\alaza\\Documents\\GitHub\\Tech-Direct-Tools\\Car\\'+assets[rand.randint(0,2)], type='string' )
    cmds.setAttr(mp+'.sideTwist', 90)    