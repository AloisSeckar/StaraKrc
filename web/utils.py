# poskytuje ruznou univerzalni funkcionalitu pro pouziti v ostatnich aplikacich
import sys

# objekt hlasky, ktera se predava z view do template a obsahuje info o zpracovani
# krom textu hlasky obsahuje take styl, jakym ma byt podbarvena (typicky 'success' pro uspech a 'danger' pro chybu)
class StatusMessage:
	def __init__(self, message, style):
		self._message = message
		self._style = style
	
	@property
	def message(self):
		return self._message
	
	@property
	def style(self):
		return self._style

# DEVELOPER FCE

# prevedeni Python vyjimky na String tak, aby bylo videt cislo problematickeho radku
def errorHelper(ex):
	return ' - ' + str(ex) + ' on line {}'.format(sys.exc_info()[-1].tb_lineno)
