## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
from CvPythonExtensions import *
import PyHelpers
import CvUtil
import ScreenInput
import CvScreenEnums
import string

PyPlayer = PyHelpers.PyPlayer
PyInfo = PyHelpers.PyInfo

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

class CvNextWarScreen:
	"Wonder Movie Screen"
	def interfaceScreen (self):
		
		self.X_SCREEN = 100
		self.Y_SCREEN = 40
		self.W_SCREEN = 775
		self.H_SCREEN = 660
		self.Y_TITLE = self.Y_SCREEN + 20
		
		self.X_EXIT = self.X_SCREEN + self.W_SCREEN/2 - 50
		self.Y_EXIT = self.Y_SCREEN + self.H_SCREEN - 43
		self.W_EXIT = 120
		self.H_EXIT = 30
		
		if (CyInterface().noTechSplash()):
			return 0
				
		player = PyPlayer(CyGame().getActivePlayer())
			
		screen = CyGInterfaceScreen( "NextWarScreen", CvScreenEnums.NEXT_WAR_SCREEN)
		screen.addPanel("NextWarPanel", "", "", true, true,
			self.X_SCREEN, self.Y_SCREEN, self.W_SCREEN, self.H_SCREEN, PanelStyles.PANEL_STYLE_MAIN)
		
		screen.showWindowBackground(True)
		screen.setRenderInterfaceOnly(False);
		screen.setSound("AS2D_NEW_ERA")
		screen.showScreen(PopupStates.POPUPSTATE_MINIMIZED, False)
		
		# Header...
		szHeader = localText.getText("TXT_KEY_NEXT_WAR_END_SCREEN", ())
		szHeaderId = "EraTitleHeader"
#		screen.setText(szHeaderId, "Background", szHeader, CvUtil.FONT_CENTER_JUSTIFY,
#			       self.X_SCREEN + self.W_SCREEN / 2, self.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.addMultilineText(szHeaderId, szHeader, self.X_SCREEN + 20, self.Y_SCREEN + 15, self.W_SCREEN - 40, 50, WidgetTypes.WIDGET_GENERAL, 669, -1, CvUtil.FONT_LEFT_JUSTIFY )
		
		screen.setButtonGFC("NextWarExit", localText.getText("TXT_KEY_MAIN_MENU_OK", ()), "", self.X_EXIT, self.Y_EXIT, self.W_EXIT, self.H_EXIT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
		
		# Show the screen
		szMovie = "Art/Interface/Screens/Next War/Earth_bad.dds"

		screen.addDDSGFC("NextWarMovie", szMovie, self.X_SCREEN + 27, self.Y_SCREEN + 68, 720, 540, WidgetTypes.WIDGET_GENERAL, -1, -1 )
				
		return 0
		
	# Will handle the input for this screen...
	def handleInput (self, inputClass):
		return 0

	def update(self, fDelta):
		return

