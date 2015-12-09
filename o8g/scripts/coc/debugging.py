from coc.log import log_calls
from coc.decorators import validate

class DebuggingDataRequests(object):
	def __init__(self, orch):
		orch.registerHandler("onLoadGameState", self.loadGameState)
		
	log_calls()
	validate(['octgn'])
	def loadGameState(self, octgn=None):
		gamestate = octgn.openUrl("http://localhost:80/debugGameState.json")