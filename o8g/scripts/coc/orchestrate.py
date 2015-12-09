import sys
import types
from coc.log import log_calls
from coc.cards import InvalidDeckException
import logging


_action_source_list = []

def event_handler(func):
	_action_source_list.append(func.__name__)
	return func


class ActionHandler(object):
	def __init__(self, name, func, id):
		self._name = name
		self._func = func
		self._id = id
		
	@property
	def Name(self):
		return self._name
		
	@property
	def Id(self):
		return self._id
	
	def __call__(self, *args, **kwargs):
		return self._func(*args, **kwargs)
	
class CardActionOrchestrator(object):
	def __init__(self, scope, octgn=None, *args, **kwargs):
		self._action_handler_list = {}
		self._id = 1
		self.octgn = octgn
		self._kwargs = kwargs
		
		self._kwargs['octgn'] = self.octgn
		
		for handler in _action_source_list:
			scope[handler] = getattr(self, handler)

	def registerHandler(self, eventName, func):
		id = self._id = self._id + 1
		if eventName not in self._action_handler_list:
			self._action_handler_list[eventName] = []
			
		self._action_handler_list[eventName].append( ActionHandler(eventName, func, id))
		
		return id
		
	def _execute(self, eventName, *args, **kwargs):
		if eventName not in self._action_handler_list:
			return
			
		continuation = True
		ckwargs = dict(self._kwargs)
		ckwargs.update(kwargs)
		for c in self._action_handler_list[eventName]:
			try:
				continuation = c(*args, **ckwargs)
			except InvalidDeckException as ide:
				self.octgn.notify(str(ide))
			except Exception as e:
				logging.getLogger("coc").debug(str(e))
			finally:
				if not continuation:
					return
	
		
	# Event Handler Root Functions
	@event_handler
	@log_calls()
	def onTableLoaded(self):
		self._execute("onTableLoaded")
		
	@event_handler
	@log_calls()
	def onGameStarted(self):
		self._execute("onGameStarted")
		
	@event_handler
	@log_calls()
	def onPlayerConnected(self, oargs):
		args = []
		kwargs = {'player':oargs.player}
		self._execute("onPlayerConnected", *args, **kwargs)

		
	@event_handler
	@log_calls()
	def onPlayerQuit(self, oargs):
		args = []
		kwargs = {'player':oargs.player}
		self._execute("onPlayerQuit", *args, **kwargs)


	@event_handler
	@log_calls()
	def onDeckLoaded(self, oargs):
		args = []
		kwargs = {'player':oargs.player, 'groups':oargs.groups}
		self._execute("onDeckLoaded", *args, **kwargs)


	@event_handler
	@log_calls()
	def onCounterChanged(self, oargs):
		args = []
		kwargs = {
			'player': oargs.player,
			'counter' : oargs.counter,
			'value' : oargs.value,
			'scripted' : oargs.scripted
		}
		self._execute("onCounterChanged", *args, **kwargs)


	@event_handler
	@log_calls()
	def onTurnPaused(self, oargs):
		args = []
		kwargs = {'player':oargs.player}
		self._execute("onTurnPaused", *args, **kwargs)


	@event_handler
	@log_calls()
	def onTurnPassed(self, oargs):
		args = []
		kwargs = {'player':oargs.player}
		self._execute("onTurnPassed", *args, **kwargs)


	@event_handler
	@log_calls()
	def onCardTargeted(self, oargs):
		args = []
		kwargs = {
			'player': oargs.player,
			'card' : oargs.card,
			'targeted' : oargs.targeted,
			'scripted' : oargs.scripted
		}
		self._execute("onCardTargeted", *args, **kwargs)


	@event_handler
	@log_calls()
	def onCardArrowTargeted(self, oargs):
		args = []
		kwargs = {
			'player': oargs.player,
			'fromCard' : oargs.fromCard,
			'toCard' : oargs.toCard,
			'targeted' : oargs.targeted,
			'scripted' : oargs.scripted
		}
		self._execute("onCardArrowTargeted", *args, **kwargs)


	@event_handler
	@log_calls()
	def onCardsMoved(self, oargs):
		cards = [
			CardMovedInfo(*info) for 
			info in 
			zip(oargs.cards, oargs.fromGroups, oargs.toGroups, oargs.indexs, oargs.xs, oargs.ys, oargs.highlights, oargs.markers, oargs.faceups)
			]

		args = []
		kwargs = {
			'player': oargs.player,
			'cards' : cards,
			'scripted' : False
		}
			
		self._execute("onCardsMoved", *args, **kwargs)


	@event_handler
	@log_calls()
	def onScriptedCardsMoved(self, oargs):
		cards = [
			CardMovedInfo(*info) for 
			info in 
			zip(oargs.cards, oargs.fromGroups, oargs.toGroups, oargs.indexs, oargs.xs, oargs.ys, oargs.highlights, oargs.markers, oargs.faceups)
			]
			
		args = []
		kwargs = {
			'player': oargs.player,
			'cards' : cards,
			'scripted' : True
		}
			
		self._execute("onCardsMoved", *args, **kwargs)


	@event_handler
	@log_calls()
	def onPlayerGlobalVariableChanged(self, oargs):
		args = []
		kwargs = {
			'player': oargs.player,
			'name' : oargs.name,
			'oldValue' : oargs.oldValue,
			'value' : oargs.value
		}
			
		self._execute("onPlayerGlobalVariableChanged", *args, **kwargs)
		

	@event_handler
	@log_calls()
	def onGlobalVariableChanged(self, oargs):
		args = []
		kwargs = {
			'name': oargs.name,
			'oldValue' : oargs.oldValue,
			'value' : oargs.value
		}
			
		self._execute("onGlobalVariableChanged", *args, **kwargs)


	@event_handler
	@log_calls()
	def onCardClicked(self, oargs):
		args = []
		kwargs = {
			'card': oargs.card,
			'mouseButton' : oargs.mouseButton,
			'keysDown' : oargs.keysDown
		}
			
		self._execute("onCardClicked", *args, **kwargs)


	@event_handler
	@log_calls()
	def onCardDoubleClicked(self, oargs):
		args = []
		kwargs = {
			'card': oargs.card,
			'mouseButton' : oargs.mouseButton,
			'keysDown' : oargs.keysDown
		}
			
		self._execute("onCardDoubleClicked", *args, **kwargs)


	@event_handler
	@log_calls()
	def onMarkerChanged(self, oargs):
		args = []
		kwargs = {
			'card': oargs.card,
			'markerName' : oargs.markerName,
			'value' : oargs.value
		}
			
		self._execute("onMarkerChanged", *args, **kwargs)

	
	@event_handler
	@log_calls()
	def onRandomDiscard(self, group):
		args = []
		kwargs = {
			'group': group
		}
			
		self._execute("onRandomDiscard", *args, **kwargs)
	
	
	@event_handler
	@log_calls()
	def onDrawCard(self, deck, x = 0, y = 0):
		args = []
		kwargs = {
			'deck': deck,
			'x' : x,
			'y' : y
		}
		
		self._execute("onDrawCard", *args, **kwargs)	
		
	@event_handler
	@log_calls()
	def onDrawMultiple(self, deck, x = 0, y = 0):
		args = []
		kwargs = {
			'deck': deck,
			'x' : x,
			'y' : y
		}
		
		self._execute("onDrawMultiple", *args, **kwargs)	
		
	@event_handler
	@log_calls()
	def onShuffle(self, cardgroup, x = 0, y = 0):
		args = []
		kwargs = {
			'cardgroup': cardgroup,
			'x' : x,
			'y' : y
		}
		
		self._execute("onShuffle", *args, **kwargs)	
		
		
	@event_handler
	@log_calls()
	def onPlayCard(self, card, x = 0, y = 0):
		args = []
		kwargs = {
			'card': card,
			'x' : x,
			'y' : y
		}
		
		self._execute("onPlayCard", *args, **kwargs)	

		
	@event_handler
	@log_calls()
	def onMoveToBottomOfDeck(self, card, x = 0, y = 0):
		args = []
		kwargs = {
			'card': card,
			'x' : x,
			'y' : y
		}
		
		self._execute("onMoveToBottomOfDeck", *args, **kwargs)	

	@event_handler
	@log_calls()
	def onToggleExhausted(self, card, x=0, y=0):
		args = []
		kwargs = {
			'card': card,
			'x' : x,
			'y' : y
		}
		
		self._execute("onToggleExhausted", *args, **kwargs)
		
		
	@event_handler
	@log_calls()
	def onSetFAQRestricted(self, group):
		self.octgn.setGlobalVariable("restricted_list", "FAQ")

	@event_handler
	@log_calls()
	def onSetAltRestricted(self, group):
		self.octgn.setGlobalVariable("restricted_list", "Alt")
		
	
	@event_handler
	@log_calls()
	def onLoadGameState(self, group):
		args = []
		kwargs = {
		}
		
		self._execute("onLoadGameState", *args, **kwargs)		

		
	@event_handler
	@log_calls()
	def onSaveGameState(self, group):
		args = []
		kwargs = {
		}
		
		self._execute("onSaveGameState", *args, **kwargs)

		
	@event_handler
	@log_calls()
	def onToggleInsanity(self, card, x=0, y=0):
		args = []
		kwargs = {
			'card': card,
			'x' : x,
			'y' : y
		}
		
		self._execute("onToggleInsanity", *args, **kwargs)
				
	
	@event_handler
	@log_calls()
	def onAddWound(self, card, x=0, y=0):
		args = []
		kwargs = {
			'card': card,
			'x' : x,
			'y' : y
		}
		
		self._execute("onAddWound", *args, **kwargs)
	
	
	@event_handler
	@log_calls()
	def onRemoveWound(self, card, x=0, y=0):
		args = []
		kwargs = {
			'card': card,
			'x' : x,
			'y' : y
		}
		
		self._execute("onRemoveWound", *args, **kwargs)
				
	
	
	
	@event_handler
	@log_calls()
	def onAddSuccess(self, card, x=0, y=0):
		args = []
		kwargs = {
			'card': card,
			'x' : x,
			'y' : y
		}
		
		self._execute("onAddSuccess", *args, **kwargs)
	
	
	@event_handler
	@log_calls()
	def onRemoveSuccess(self, card, x=0, y=0):
		args = []
		kwargs = {
			'card': card,
			'x' : x,
			'y' : y
		}
		
		self._execute("onRemoveSuccess", *args, **kwargs)

	
	@event_handler
	@log_calls()
	def onDiscardCard(self, card, x=0, y=0):
		args = []
		kwargs = {
			'card': card,
			'x' : x,
			'y' : y
		}
		
		self._execute("onDiscardCard", *args, **kwargs)
		
		
		
class CardMovedInfo(object):
	def __init__(self, card, fromGroup, toGroup, index, x, y, highlight, marker, faceup):
		self.card = card
		self.fromGroup = fromGroup
		self.toGroup = toGroup
		self.index = index
		self.x = x
		self.y = y
		self.highlight = highlight
		self.marker = marker
		self.faceup = faceup
		
		
	