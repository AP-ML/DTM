## Basic Inquisition v1.0 by modifieda4 2011

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
import CvEventInterface



# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer
PyInfo = PyHelpers.PyInfo
PyCity = PyHelpers.PyCity
PyGame = PyHelpers.PyGame

gPerReligionBonus = 10 		#per religion purged in a city get this gold
gProductionCostModifier = 0.2	#percentage production cost per religious bulding purged
gPopulationBonus = 3  		#get this times the cities population in gold per inquisition

def doInquisitorPersecution(pCity, pUnit):
	pPlayer = gc.getPlayer( pCity.getOwner( ) )
	iPlayer = pPlayer.getID( )		
	# gets a list of all religions in the city except state religion
	#CyInterface().playGeneralSound("AS3D_UN_CHRIST_MISSIONARY_ACTIVATE")
	lCityReligions = [ ]
	for iReligionLoop in range(gc.getNumReligionInfos( )):
		if pCity.isHasReligion( iReligionLoop ):
			if pPlayer.getStateReligion( ) != iReligionLoop:
				lCityReligions.append( iReligionLoop )
				iHC = 0
				if pCity.isHolyCityByType(iReligionLoop):
					iHC = -50
			else:
				if pCity.isHolyCityByType(iReligionLoop):
					iHC = 10
	# Does Persecution succeed
	iGoldBack = 0
	irandom = gc.getGame().getSorenRandNum(100,"")
	if irandom < 95 - ((len( lCityReligions ))*5) + iHC:
		# increases Anger for all AIs in City Religion List
		#BugUtil.alert("increasing AI anger")
		if len( lCityReligions ) > 0:				
			for iAI_PlayersLoop in range(gc.getMAX_PLAYERS()):
				pSecondPlayer = gc.getPlayer(iAI_PlayersLoop)	
				iSecondPlayer = pSecondPlayer.getID( )
				#BugUtil.alert("increasing AI anger")
				for iAIAngerLoop in range( len( lCityReligions ) ):
					pReligion = gc.getReligionInfo( lCityReligions[iAIAngerLoop] )
					if pSecondPlayer.getStateReligion( ) == lCityReligions[iAIAngerLoop]:							
						pSecondPlayer.AI_changeAttitudeExtra( pPlayer.getID( ), -1 )
						CyInterface().addMessage(iSecondPlayer,False,25,CyTranslator().getText("TXT_KEY_MESSAGE_INQUISITION_GLOBAL",(pCity.getName(),pReligion.getText())),"AS2D_PLAGUE",InterfaceMessageTypes.MESSAGE_TYPE_INFO,pUnit.getButton(),ColorTypes(7),pCity.getX(),pCity.getY(),True,True)
					else:
						if iSecondPlayer != iPlayer:
							#To do: add happiness to other players
							lCities = PyPlayer( iSecondPlayer ).getCityList( )
							for iCityloop in range( pSecondPlayer.getNumCities() ):
								pPlayerCity = lCities[ iCityloop ]
								if pPlayerCity.isHolyCityByType(lCityReligions[iAIAngerLoop]):
									CyInterface().addMessage(iSecondPlayer,False,25,CyTranslator().getText("TXT_KEY_MESSAGE_INQUISITION_GLOBAL",(pCity.getName(),pReligion.getText())),"AS2D_PLAGUE",InterfaceMessageTypes.MESSAGE_TYPE_INFO,pUnit.getButton(),ColorTypes(7),pCity.getX(),pCity.getY(),True,True)

		# removes buildings
		for iBuildingLoop in range(gc.getNumBuildingInfos( )):
			if pCity.isHasBuilding( iBuildingLoop ):
				pBuilding = gc.getBuildingInfo( iBuildingLoop )
				iRequiredReligion = pBuilding.getPrereqReligion( )
				for iReligionLoop in range(gc.getNumReligionInfos()):
					if iReligionLoop != pPlayer.getStateReligion( ):
						if iRequiredReligion == iReligionLoop:
							#Removes building 
							pCity.setNumRealBuilding ( iBuildingLoop,0 )
							#Calculates cost							
							iGoldBack = iGoldBack + int(pBuilding.getProductionCost()*gProductionCostModifier)

		# Loop through all religions, remove them from the city
		for iReligionLoop in range(gc.getNumReligionInfos()):
			if iReligionLoop != pPlayer.getStateReligion( ):				
				if pCity.isHolyCityByType( iReligionLoop ):
					gc.getGame( ).clearHolyCity( iReligionLoop )
				if pCity.isHasReligion(iReligionLoop):
					iGoldBack=iGoldBack + gPerReligionBonus					
			pCity.setHasReligion(iReligionLoop, 0, 0, 0)

		#calculates population bonus
		iGoldBack = iGoldBack + pCity.getPopulation()*gPopulationBonus
	
		
		# Add player's state religion
		if ( gc.getPlayer( pUnit.getOwner( ) ).getStateReligion( ) != -1 ):
			iStateReligion = gc.getPlayer( pUnit.getOwner( ) ).getStateReligion( )
			pCity.setHasReligion( iStateReligion, 1, 0, 0 )

		# Persecution succeeds
		CyInterface().addMessage(CyGame().getActivePlayer(),False,25,CyTranslator().getText("TXT_KEY_MESSAGE_INQUISITION",(pCity.getName(),)),"AS2D_PLAGUE",InterfaceMessageTypes.MESSAGE_TYPE_INFO,pUnit.getButton(),ColorTypes(8),pCity.getX(),pCity.getY(),True,True)
		
		# confiscate
		if iGoldBack>0:
			pPlayer.changeGold(iGoldBack)
			if pPlayer.isHuman():				
				CyInterface().addMessage(CyGame().getActivePlayer(),False,25,CyTranslator().getText("TXT_KEY_MESSAGE_INQUISITION_CONFISCATION",(str(iGoldBack),)),"",InterfaceMessageTypes.MESSAGE_TYPE_INFO,pUnit.getButton(),ColorTypes(6),pCity.getX(),pCity.getY(),True,True)
		
						
	# Persecution fails
	else:
		#CyInterface().addMessage(iPlayer,False,25,CyTranslator().getText("TXT_KEY_MESSAGE_INQUISITION_FAIL",(pCity.getName(),)),"AS2D_SABOTAGE",InterfaceMessageTypes.MESSAGE_TYPE_INFO,pUnit.getButton(),ColorTypes(7),pCity.getX(),pCity.getY(),True,True)
		CyInterface().addMessage(CyGame().getActivePlayer(),False,25,CyTranslator().getText("TXT_KEY_MESSAGE_INQUISITION_FAIL",(pCity.getName(),)),"AS2D_SABOTAGE",InterfaceMessageTypes.MESSAGE_TYPE_INFO,pUnit.getButton(),ColorTypes(7),pCity.getX(),pCity.getY(),True,True)

	# Unit expended
	pUnit.kill( 0, -1 )



