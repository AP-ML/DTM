## Basic Inquisition v1.2 by modifieda4 2012

from CvPythonExtensions import *
import CvUtil
import CvScreensInterface
import CvDebugTools
import CvWBPopups
import PyHelpers
import Popup as PyPopup
import CvCameraControls
import CvTopCivs
import sys
import CvWorldBuilderScreen
import CvAdvisorUtils
import CvTechChooser
import pickle
import BugCore
import BugUtil
import SdToolkit
import BasicInquisitionGameUtils


# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer
PyInfo = PyHelpers.PyInfo
PyCity = PyHelpers.PyCity
PyGame = PyHelpers.PyGame

class BasicInquisitionEvent:

	def __init__(self, eventMgr):
		self.eventMgr = eventMgr
        	#eventMgr.addEventHandler("InquisitorPersecution", self.doInquisitorPersecution)
		eventMgr.addEventHandler("ModNetMessage", self.onModNetMessage)


	def onModNetMessage(self, argsList):
			
		iData1, iData2, iData3, iData4, iData5 = argsList		

		iMessageID = iData1
		
		# Launch Inquisition!
		if (iMessageID == 665):
			
			iPlotX = iData2
			iPlotY = iData3
			iOwner = iData4
			iUnitID = iData5
			
			pPlot = CyMap( ).plot( iPlotX, iPlotY )
			pCity = pPlot.getPlotCity( )
			pPlayer = gc.getPlayer( iOwner )
			pUnit = pPlayer.getUnit( iUnitID )
			#BugUtil.alert("Inquisition Alert")			
			BasicInquisitionGameUtils.doInquisitorPersecution( pCity, pUnit )			



def cannotTrain(argsList):
	pCity = argsList[0]
	eUnit = argsList[1]
	bContinue = argsList[2]
	bTestVisible = argsList[3]
	bIgnoreCost = argsList[4]
	bIgnoreUpgrades = argsList[5]
	ePlayer = pCity.getOwner()
	pPlayer = gc.getPlayer(ePlayer)

	if eUnit == gc.getInfoTypeForString('UNIT_INQUISITOR'):
		if pPlayer.getCivics(gc.getInfoTypeForString('CIVICOPTION_RELIGION')) != gc.getInfoTypeForString('CIVIC_THEOCRACY'):
			return True
	return False

def AI_chooseProduction(argsList):
	pCity = argsList[0]

	## Inquisitor Production AI ##
	
	iOwner = pCity.getOwner( )
	pPlayer = gc.getPlayer( pCity.getOwner( ) )
	iInquisitor = CvUtil.findInfoTypeNum( gc.getUnitInfo, gc.getNumUnitInfos(), "UNIT_INQUISITOR" )
	iStateReligion = gc.getPlayer( iOwner ).getStateReligion( )	
	#Checks religion percents
	lReligions = [ ]
	bestReligionPercent = 0
	iStateLevel = 0
	for iReligionLoop in range(gc.getNumReligionInfos( )):
		if (gc.getGame().getReligionGameTurnFounded(iReligionLoop) > 0):
			iReligionLevel = gc.getGame().calculateReligionPercent(iReligionLoop)
			if iStateReligion >= 0:
				iStateLevel = gc.getGame().calculateReligionPercent(iStateReligion)
			if iReligionLevel > iStateLevel:
				lReligions.append( iReligionLoop )
			if (iReligionLoop != iStateReligion):
				religionPercent = gc.getGame().calculateReligionPercent(iReligionLoop)
				if (religionPercent > bestReligionPercent):
					bestReligionPercent = religionPercent

	if iStateReligion >= 0 or bestReligionPercent >= 60:
		if pCity.canTrain( iInquisitor, 0, 0 ):
			lUnits = PyPlayer( pPlayer.getID( ) ).getUnitList( )
			for iUnit in range( len( lUnits) ):
				# if there are any Inquisitors, don't Build one
				if pPlayer.getUnit( lUnits[ iUnit ].getID( ) ).getUnitType( ) == iInquisitor:
					return False
			if getRandomNumber(2) == 0:
				gc.getMap( ).plot( pCity.getX( ), pCity.getY( ) ).getPlotCity( ).pushOrder( OrderTypes.ORDER_TRAIN, iInquisitor, -1, False, False, False, True )
				#BugUtil.alert("AI deciding to produce inquisitor by player %s", iOwner)
				return True	

	return False

	## Inquisitor Productions AI ##

def AI_unitUpdate(argsList):
	pUnit = argsList[0]
	iOwner = pUnit.getOwner( )
	iInquisitor = CvUtil.findInfoTypeNum( gc.getUnitInfo, gc.getNumUnitInfos(), "UNIT_INQUISITOR" )
		
	if not gc.getPlayer( iOwner ).isHuman( ):
		if pUnit.getUnitType( ) == iInquisitor:
			doInquisitorCore_AI( pUnit )
			return True
	return False

def getWidgetHelp(argsList):
	eWidgetType, iData1, iData2, bOption = argsList
	if iData1 == 665:
		return CyTranslator().getText("TXT_KEY_GODS_INQUISTOR_CLEANSE_MOUSE_OVER", ())		
	return u""

def doInquisitorCore_AI(pUnit):
	iOwner = pUnit.getOwner( )
	iStateReligion = gc.getPlayer( iOwner ).getStateReligion( )
	lCities = PyPlayer( iOwner ).getCityList( )
        pPlayer = gc.getPlayer(iOwner)
	

	if pPlayer.getCivics(gc.getInfoTypeForString('CIVICOPTION_RELIGION')) == gc.getInfoTypeForString('CIVIC_THEOCRACY'):	
		#Looks to see if the AI controls a City that has a non-State Religion
		for iCity in range( len( lCities ) ):
			for iReligion in range( gc.getNumReligionInfos( ) ):
				if iReligion != iStateReligion:
					pCity = gc.getPlayer( iOwner ).getCity( lCities[ iCity ].getID( ) )
					if pCity.isHasReligion( iReligion ) and pCity.isHasReligion( iStateReligion ):
						#Makes the unit move to the City and purge it
						if pUnit.generatePath( pCity.plot( ), 0, False, None ):
							doHolyCitySeekAndDestroy( pUnit, pCity )
							#BugUtil.alert("AI decided to purge: player %s", iOwner)
							return		
		
		#Looks to see if the AI controls a Holy City that is not the State Religion
		for iCity in range( len( lCities ) ):
			for iReligion in range( gc.getNumReligionInfos( ) ):
				if iReligion != iStateReligion:
					pCity = gc.getPlayer( iOwner ).getCity( lCities[ iCity ].getID( ) )
					if pCity.isHolyCityByType( iReligion ) and pCity.isHasReligion( iStateReligion ):
						#Makes the unit move to the City and purge it
						if pUnit.generatePath( pCity.plot( ), 0, False, None ):
							doHolyCitySeekAndDestroy( pUnit, pCity )
							#BugUtil.alert("AI decided to purge holy city: player %s", iOwner)
							return
	
def doHolyCitySeekAndDestroy(pUnit, pCity ):
		
	if pUnit.getX( ) != pCity.getX( ) or pUnit.getY( ) != pCity.getY( ):
		pUnit.getGroup().pushMission(MissionTypes.MISSION_MOVE_TO, pCity.getX( ), pCity.getY( ), 0, False, True, MissionAITypes.NO_MISSIONAI, pUnit.plot(), pUnit)
	else:	
		BasicInquisitionGameUtils.doInquisitorPersecution( pCity, pUnit )
	

def getRandomNumber(int):
	return CyGame().getSorenRandNum(int, "Gods_CvGameUtils")	