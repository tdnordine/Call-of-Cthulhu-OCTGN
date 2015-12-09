import sys

class Octgn(object):
	_octgn_methods = [
		"askCard",
		"cardDlg",
		"askChoice",
		"askInteger",
		"askMarker",
		"askString",
		"currentGameName",
		"confirm",
		"gameVersion",
		"getGlobalVariable",
		"getSetting",
		"mute",
		"notify",
		"notifyBar",
		"openUrl",
		"getPlayers",
		"playSound",
		"remoteCall",
		"resetGame",
		"rnd",
		"setGlobalVariable",
		"setSetting",
		"turnNumber",
		"version",
		"webRead",
		"whisper",
		"update",
		"me",
		"table"
	]
	
	def __init__(self, scope):
		self.octgn = {name : scope[name] for name in self._octgn_methods}
		
	def __getattr__(self, attr):
		if attr in self.octgn:
			return self.octgn[attr]
			
		return None
