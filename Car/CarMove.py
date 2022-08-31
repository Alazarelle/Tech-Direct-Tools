import maya.cmds as cmds
from random import uniform as rand
from mtoa.core import createStandIn

#create curve
path = cmds.curve( p=[(-868, 0, 736), (-325, 0,725), (261, 0, 698), (577, 0, 701), (726, 0, 426), (721, 0, -312), (729, 0, -536), (720, 0, -851)] )

#multiple cars amount
carAmount = int(input('Enter amounnt of cars to generate: '))
print(carAmount)

#select end keyframe
endFrame = int(input('Speed: '))
print(endFrame)

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
        cmds.move(0,0,300, standIn, relative=True)
    #disconnect set u value
    cmds.disconnectAttr(mp+'_uValue.output', mp+'.uValue')
    #create Speed Controller
    speedCont = cmds.group( em=True, name='SpeedControllor' )
    cmds.addAttr( longName='speed', defaultValue=0, minValue=0, maxValue=5)
    #connect speed to motion path u val
    cmds.connectAttr(speedCont+'.speed', mp+'.uValue')
    #set key frames start
    num = rand(12,16)
    cmds.currentTime(car*num)
    cmds.setAttr( speedCont+'.speed', 0 )
    cmds.setKeyframe(speedCont+'.speed')
    #set key frame end
    cmds.currentTime(endFrame+(car*num))
    cmds.setAttr( speedCont+'.speed', 5 )
    cmds.setKeyframe(speedCont+'.speed')
    #import car standin
    cmds.setAttr( standIn+'.dso','E:\TechDirection\Car\car01_v002.ass', type='string' )
    cmds.setAttr(mp+'.sideTwist', 90)    