from coc.log import log_calls
from coc.decorators import validate


class PlayerActionHandler(object):
	def __init__(self, oct):
		oct.registerHandler("onDrawCard", self.draw1)
		oct.registerHandler("onDrawMultiple", self.drawX)
		oct.registerHandler("onShuffle", self.shuffleDeck)

	@log_calls()
	@validate(['deck', 'octgn'])
	def draw1(self, deck=None, octgn=None, *args, **kwargs):
		
		card = deck.top()
		card.moveTo(octgn.me.hand)
		
		return False
		
	@log_calls()
	@validate(['deck', 'octgn'])
	def drawX(self, deck=None, octgn=None, *args, **kwargs):
		count = octgn.askInteger("How Many Cards?", 2)
		
		for x in range(count):
			card = deck.top()
			card.moveTo(octgn.me.hand)
			
		return False
		
	@log_calls()
	@validate(['octgn'])	
	def shuffleDeck(self, octgn=None, *args, **kwargs):
		octgn.whisper("Going to Shuffle The Deck Now!!!!")
		octgn.me.deck.shuffle()
		
		return False
