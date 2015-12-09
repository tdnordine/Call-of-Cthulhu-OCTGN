
_event_names = [
    ("onTableLoaded", "OnTableLoaded"),
    ("onGameStarted", "OnGameStarted"),
    ("onPlayerConnected", "OnPlayerConnected"),
    ("onPlayerQuit", "OnPlayerQuit"),
    ("onDeckLoaded", "OnDeckLoaded"),
    ("onCounterChanged", "OnCounterChanged"),
    ("onTurnPaused", "OnTurnPaused"),
    ("onTurnPassed", "OnTurnPassed"),
    ("onCardTargeted", "OnCardTargeted"),
    ("onCardArrowTargeted", "OnCardArrowTargeted"),
    ("onCardsMoved", "OnCardsMoved"),
    ("onScriptedCardsMoved", "OnScriptedCardsMoved"),
    ("onPlayerGlobalVariableChanged", "OnPlayerGlobalVariableChanged"),
    ("onGlobalVariableChanged", "OnGlobalVariableChanged"),
    ("onCardClicked", "OnCardClicked"),
    ("onCardDoubleClicked", "OnCardDoubleClicked"),
    ("onMarkerChanged", "OnMarkerChanged")
]

class EventHandler(object):
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
	
	def trigger(self, octgn, args):
		return self._func(octgn, args)
		

class Events(object):
	def __init__(self, octgn):
		self._event_list = []
		self._id = 1
		self._octgn = octgn
		
	def registerHandler(self, eventName, func):
		self._event_list.append( EventHandler(eventName, func, self._id))
		self._id = self._id + 1
		
	def unregisterHandler(self, id):
		self._event_list = [c for c in self._event_list if c.ID != id]
		
	def trigger(self, name, args):
		continuation = True
		for c in self._event_list:
			if c.Name == name:
				continuation = c.trigger(self._octgn, args)

			if not continuation:
				return

def _createHandlerFunction(evts, name, octgn):
	def _handlerFunc(args=None):
		octgn.whisper("{} was called.".format(name));
		evts.trigger(name, args)
	
	_handlerFunc.__name__ = name
	return _handlerFunc

def _createEventHandlers(mod, evts, octgn):
	for e in _event_names:
		mod[e[0]] = _createHandlerFunction(evts, e[1], octgn)
		
		
# decorators
def register(eventName, evts):
	def _register(func):
		evts.registerHandler(eventName, func)
		return func
	return _register
		
	
def isMe(func):
	def _isMeImpl(octgn, args):
		octgn.whisper("isMe Called")

		if octgn.me == args.player:
			return func(octgn, args)
		return True
	return _isMeImpl

def isMyCard(func):
	def _isMyCardImpl(octgn, args):
		octgn.whisper("isMyCard Called")
		
		if octgn.me == args.card.owner:
			return func(octgn, args)
		return True

	return _isMyCardImpl
	
#root handlers
#def onTableLoaded():
#	debug("{} was called.".format(onTableLoaded.__name__));
#	events.trigger("OnTableLoaded", None)
#	
#def onGameStarted():
#	debug("{} was called.".format(onGameStarted.__name__));
#	events.trigger("OnGameStarted", None)
#	
#def onPlayerConnected(args):
#	debug("{} was called. {} was connected.".format(onPlayerConnected.__name__, args.player));
#	events.trigger("OnPlayerConnected", args)
#	
#def onPlayerQuit(args):
#	debug("{} was called. {} quit the game.".format(onPlayerQuit.__name__, args.player));
#	events.trigger("OnPlayerQuit", args)
#	
#def onDeckLoaded(args):
#	debug("{} was called. {} loaded a deck.".format(onDeckLoaded.__name__, args.player));
#	events.trigger("OnDeckLoaded", args)
#	
#def onCounterChanged(args):
#	debug("{} was called. {} changed counter {} to {}.".format(onCounterChanged.__name__, args.player, args.counter, args.counter.value));
#	events.trigger("OnCounterChanged", args)
#	
#def onTurnPaused(args):
#	debug("{} was called. {} paused the turn.".format(onTurnPaused.__name__, args.player));
#	events.trigger("OnTurnPaused", args)
#
#def onTurnPassed(args):
#	debug("{} was called. {} passed the turn.".format(onTurnPassed.__name__, args.player));
#	events.trigger("OnTurnPassed", args)
#	
#def onCardTargeted(args):
#	debug("{} was called. {} targeted the card {}".format(onCardTargeted.__name__, args.player, args.card));
#	events.trigger("OnCardTargeted", args)
#	
#def onCardArrowTargeted(args):
#	debug("{} was called. {} drew an arrow between {} and {}".format(onCardArrowTargeted.__name__, args.player, args.fromCard, args.toCard));
#	events.trigger("OnCardArrowTargeted", args)
#	
#def onCardsMoved(args):
#	debug("{} was called. {} moved the cards {}".format(onCardsMoved.__name__, args.player, str([c.name for c in args.cards])));
#	events.trigger("OnCardsMoved", args)
#	
#def onScriptedCardsMoved(args):
#	debug("{} was called. {} moved the cards {}".format(onScriptedCardsMoved.__name__, args.player, str([c.name for c in args.cards])));
#	events.trigger("OnScriptedCardsMoved", args)
#	
#def onPlayerGlobalVariableChanged(args):
#	debug("{} was called. {}'s variable {} changed from {} to {}".format(onPlayerGlobalVariableChanged.__name__, args.player, args.name, args.oldValue, args.value));
#	events.trigger("OnPlayerGlobalVariableChanged", args)
#	
#def onGlobalVariableChanged(args):
#	debug("{} was called. {} Global variable changed from {} to {}".format(onGlobalVariableChanged.__name__, args.name, args.oldValue, args.value));
#	events.trigger("OnGlobalVariableChanged", args)
#	
#def onCardClicked(args):
#	debug("{} was called. {} was clicked".format(onCardClicked.__name__, args.card));
#	events.trigger("OnCardClicked", args)
#	
#def onCardDoubleClicked(args):
#	debug("{} was called. {} was double clicked".format(onCardDoubleClicked.__name__, args.card));
#	events.trigger("OnCardDoubleClicked", args)
#	
#def onMarkerChanged(args):
#	debug("{} was called. {} on card {} was changed to {}".format(onMarkerChanged.__name__, args.markerName, args.card, args.value));
#	events.trigger("OnMarkerChanged", args)
#	

