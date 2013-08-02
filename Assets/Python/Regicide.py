## Sid Meier's Civilization 4
## Copyright Firaxis Games 2007

from CvPythonExtensions import *
from PyHelpers import PyPlayer

gc = CyGlobalContext()

class Regicide:
	def Death(self, iPlayer, pUnit):
		pPlayer = gc.getPlayer(iPlayer)
		iAnarchy = gc.getDefineINT("GOLDEN_AGE_LENGTH") * gc.getGameSpeedInfo(CyGame().getGameSpeedType()).getGoldenAgePercent() /100
		pPlayer.changeAnarchyTurns(iAnarchy)
		CyInterface().addMessage(iPlayer,True,15,CyTranslator().getText("TXT_KEY_KING_DIED",()),'',0, gc.getUnitCombatInfo(gc.getInfoTypeForString("UNITCOMBAT_KING")).getButton(), gc.getInfoTypeForString("COLOR_WARNING_TEXT"), pUnit.getX(), pUnit.getY(), True,True)
		lMaster = []
		lVassal = []
		for iTeamX in xrange(gc.getMAX_CIV_TEAMS()):
			if iTeamX == pPlayer.getTeam(): continue
			pTeamX = gc.getTeam(iTeamX)
			if pTeamX.getUnitClassCount(gc.getInfoTypeForString("UNITCLASS_KING")) > 0:
				if pTeamX.isAVassal():
					lVassal.append(iTeamX)
				else:
					lMaster.append(iTeamX)
		if len(lMaster) == 0 and len(lVassal) == 1:
			CyGame().setWinner(lVassal[0], gc.getInfoTypeForString("VICTORY_REGICIDE"))
		elif len(lMaster) == 1:
			bVictory = True
			for iVassal in lVassal:
				if gc.getTeam(iVassal).isVassal(lMaster[0]): continue
				bVictory = False
			if bVictory:
				CyGame().setWinner(lMaster[0], gc.getInfoTypeForString("VICTORY_REGICIDE"))

	def Birth(self, pCity):
		lFemale = [gc.getInfoTypeForString("LEADER_BOUDICA"), gc.getInfoTypeForString("LEADER_HATSHEPSUT"), gc.getInfoTypeForString("LEADER_ELIZABETH"), 
			gc.getInfoTypeForString("LEADER_VICTORIA"), gc.getInfoTypeForString("LEADER_CATHERINE"), gc.getInfoTypeForString("LEADER_ISABELLA")]

		iPlayer = pCity.getOwner()
		pPlayer = gc.getPlayer(iPlayer)
		iLeaderType = pPlayer.getLeaderType()
		if iLeaderType in lFemale:
			pUnit = pPlayer.initUnit(gc.getInfoTypeForString("UNIT_QUEEN"), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.NO_DIRECTION)
			pUnit.setLeaderUnitType(gc.getInfoTypeForString("UNIT_FEMALE_GREAT_GENERAL"))
		else:
			pUnit = pPlayer.initUnit(gc.getInfoTypeForString("UNIT_KING"), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.NO_DIRECTION)
			pUnit.setLeaderUnitType(gc.getInfoTypeForString("UNIT_GREAT_GENERAL"))
		pUnit.setName(pPlayer.getName())
		pUnit.setBaseCombatStr(pPlayer.getNumCities() * (pPlayer.getCurrentEra() + 1))
		self.addTraitPromotions(pUnit, pPlayer)
		pUnit.finishMoves()

	def addTraitPromotions(self, pUnit, pPlayer):
		if pPlayer.hasTrait(gc.getInfoTypeForString("TRAIT_AGGRESSIVE")):
			pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_COMBAT1"), True)
		if pPlayer.hasTrait(gc.getInfoTypeForString("TRAIT_PROTECTIVE")):
			pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_CITY_GARRISON1"), True)
		if pPlayer.hasTrait(gc.getInfoTypeForString("TRAIT_EXPANSIVE")):
			pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_MOBILITY"), True)
		if pPlayer.hasTrait(gc.getInfoTypeForString("TRAIT_IMPERIALIST")):
			pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_DRILL1"), True)
		if pPlayer.hasTrait(gc.getInfoTypeForString("TRAIT_CHARISMATIC")):
			pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_LEADERSHIP"), True)
		if pPlayer.hasTrait(gc.getInfoTypeForString("TRAIT_SPIRITUAL")):
			pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_MEDIC1"), True)
		if pPlayer.hasTrait(gc.getInfoTypeForString("TRAIT_INDUSTRIOUS")):
			pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_ACCURACY"), True)
		if pPlayer.hasTrait(gc.getInfoTypeForString("TRAIT_ORGANIZED")):
			pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_FLANKING1"), True)
		if pPlayer.hasTrait(gc.getInfoTypeForString("TRAIT_PHILOSOPHICAL")):
			pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_MARCH"), True)
		if pPlayer.hasTrait(gc.getInfoTypeForString("TRAIT_CREATIVE")):
			pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_BARRAGE1"), True)
		if pPlayer.hasTrait(gc.getInfoTypeForString("TRAIT_FINANCIAL")):
			pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_CITY_RAIDER1"), True)
		if pPlayer.hasTrait(gc.getInfoTypeForString("TRAIT_PRODUCTIVE")):
			pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_TACTICS"), True)
		if pPlayer.hasTrait(gc.getInfoTypeForString("TRAIT_SCIENTIFIC")):
			pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_SENTRY"), True)
		if pPlayer.hasTrait(gc.getInfoTypeForString("TRAIT_HUMANITARIAN")):
			pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_MORALE"), True)
		if pPlayer.hasTrait(gc.getInfoTypeForString("TRAIT_DECEITFUL")):
			pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_GUERILLA1"), True)
		if pPlayer.hasTrait(gc.getInfoTypeForString("TRAIT_COMMERCIAL")):
			pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_COMMANDO"), True)
		if pPlayer.hasTrait(gc.getInfoTypeForString("TRAIT_SEAFARING")):
			pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_AMPHIBIOUS"), True)
		if pPlayer.hasTrait(gc.getInfoTypeForString("TRAIT_EQUESTRIAN")):
			pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_WOODSMAN1"), True)
			
	def setKingStr(self, pPlayer, iNumCities):
		(loopUnit, iter) = pPlayer.firstUnit(False)
		while(loopUnit):
			if loopUnit.getUnitClassType() == gc.getInfoTypeForString("UNITCLASS_KING"):
				loopUnit.setBaseCombatStr(iNumCities * (pPlayer.getCurrentEra() + 1))
				break
			(loopUnit, iter) = pPlayer.nextUnit(iter, False)

	def doEraCheck(self, iTeam, iTechType):
		bNewEra = True
		for iTech in xrange(gc.getNumTechInfos()):
			if gc.getTeam(iTeam).isHasTech(iTech) and iTech != iTechType:
				if gc.getTechInfo(iTech).getEra() >= gc.getTechInfo(iTechType).getEra():
					bNewEra = False
					break
		if bNewEra:
			for iPlayerX in xrange(gc.getMAX_CIV_PLAYERS()):
				pPlayerX = gc.getPlayer(iPlayerX)
				if pPlayerX.getTeam() != iTeam: continue
				if pPlayerX.getUnitClassCount(gc.getInfoTypeForString("UNITCLASS_KING")) == 0: continue
				self.setKingStr(pPlayerX, pPlayerX.getNumCities())