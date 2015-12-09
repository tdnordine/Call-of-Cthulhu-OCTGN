from coc.log import log_calls
from coc.decorators import validate, isMine

class InvalidDeckException(Exception):
	def __init__(self, msg):
		Exception.__init__(self, msg)

		
class CardActionHandler(object):
	_current_banned_cards = [
	]
	_current_restricted_cards = [
		"Itinerant Scholar", # Itinerant Scholar (Core F30)
		"Ravager from the Deep", # Ravager from the Deep (Core F46)
		"Shocking Transformation", # Shocking Transformation (Core F140)
		"Diseased Sewer Rats", # Diseased Sewer Rats (Secrets of Arkham F44)
		"Broken Space, Broken Time", # Broken Space, Broken Time (Forgotten Lore F59)
		"Infernal Obsession", # Infernal Obsession  (Summons of the Deep F51)
		"Twilight Gate", # Twilight Gate (Dreamlands F12)
		"Dreamlands Fanatic", # Dreamlands Fanatic (Dreamlands F47)
		"Guardian Pillar", # Guardian Pillar (Dreamlands F78)
		"Obsessive Insomniac", # Obsessive Insomniac (Dreamlands F110)
		"Nyarlathotep", # Nyarlathotep  (Dreamlands F117)
		"Speak to the Dead", # Speak to the Dead (The Yuggoth Contract F20)
		"Museum Curator", # Museum Curator (The Yuggoth Contract F70)
		"Doppelganger", # Doppelganger (The Yuggoth Contract F79)
		"Khopesh of the Abyss", # Khopesh of the Abyss (Ancient Relics F16)
		"Temple of R'lyeh", # Temple of R'lyeh (Ancient Relics F73)
		"Stygian Eye", # Stygian Eye (Ancient Relics F96)
		"Master of the Myths", # Master of the Myths (Ancient Relics F101)
		"Uroborus", # Uroborus (Revelations F3)
		"Feed Her Young", # Feed Her Young (Revelations F11)
		"Marcus Jamburg", # Marcus Jamburg (Revelations F40)
		"Matthew Alexander", # Matthew Alexander (Seekers of Knowledge F7) 
		"Alternative Historian", # Alternative Historian (Seekers of Knowledge F15)
		"Por XV 14:19", # Por XV 14:19 (Seekers of Knowledge F44)
		"Nikola Tesla", # Nikola Tesla (The Key and the Gate F4)
		"Lost Oracle", # Lost Oracle (The Key and the Gate F9)
		"Yithian Scout", # Yithian Scout (The Key and the Gate F15)
		"Rite of the Silver Gate", # Rite of the Silver Gate (The Key and the Gate F25)
		"Studying the Void", # Studying the Void (The Key and the Gate F35)
		"Interstellar Migration", # Interstellar Migration (The Key and the Gate F37)
		"The Festival", # The Festival (The Key and the Gate F51)
		"Josef Meiger"  # Josef Meiger (Denizens of the Underworld F52)
	]
	
	_tom_proposed_banned_cards = [
		"Nikola Tesla", # Nikola Tesla (The Key and the Gate F4)
		"Interstellar Migration" # Interstellar Migration (The Key and the Gate F37)
	]
	
	_tom_proposed_restricted_cards = [
	]
	
	_markerWound = ("Wound", "4a247d69-b2cc-4de9-b4d1-c447bea01f61")
	_markerSuccess = ("Success", "4a247d69-b2cc-4de9-b4d1-c447bea01f62")

	def __init__(self, orch):
		orch.registerHandler("onToggleExhausted", self.toggleExhausted)
		orch.registerHandler("onDeckLoaded", self.validateDeck)
		orch.registerHandler("onGlobalVariableChanged", self.setRestricted)
		orch.registerHandler("onAddWound", self.addWound)
		orch.registerHandler("onRemoveWound", self.removeWound)
		orch.registerHandler("onAddSuccess", self.addSuccess)
		orch.registerHandler("onRemoveSuccess", self.removeSuccess)
		
		
		self.banned_cards = self._current_banned_cards
		self.restricted_cards = self._current_restricted_cards
		
	@log_calls()
	@validate(['card'])
	def toggleExhausted(self, card=None):
		return True
		
	@log_calls()
	@validate(['name=restricted_list', 'oldValue', 'value'])
	def setRestricted(self, name="", oldValue="", value="FAQ", *args, **kwargs):
		if value is 'FAQ':
			self.banned_cards = self._current_banned_cards
			self.restricted_cards = self._current_restricted_cards
		elif value is 'Alt':
			self.banned_cards = self._tom_proposed_banned_cards
			self.restricted_cards = self._tom_proposed_restricted_cards
				
		return True
		
	
	def _accumulate(self, contain, card):
		name = card.name.strip('[]?_{}<>^* ')
		
		if name not in contain:
			contain[name] = 0
			
		contain[name] = contain[name] + 1
		return contain
		
	def _restricted(self, container, item):
		if item in self.restricted_cards:
			container.append(item)
		return container
	
	def _banned(self, container, item):
		if item in self.banned_cards:
			container.append(item)
		return container
		
	@log_calls()
	@validate(['octgn', 'groups'])
	@isMine
	def validateDeck(self, octgn=None, groups=None, *args, **kwargs):
		with octgn.mute():
			
			spile = octgn.me.piles['ScriptingPile']
			
			for group in groups:
				for card in group:
					card.moveTo( spile )
			
			acc_deck = reduce(self._accumulate, spile, {})
			# move the cards to the deck since we are done with them now.
			for card in spile:
				card.moveTo( octgn.me.deck )

			#must have 50+ cards
			if len(octgn.me.deck) < 50:
				raise InvalidDeckException("Invalid Deck. Deck Loaded by {} has only {} cards. It must have 50 or more.".format(octgn.me, len(octgn.me.deck)))
				
			#must not have more then 3 copies of each card
			counts = [ val for val in acc_deck.items() if val[1] > 3 ]
			
			if len(counts) > 0:
				raise InvalidDeckException("Invalid Deck. Deck Loaded by {} contains {} copies of {}.".format(octgn.me, counts[0][1], counts[0][0]))
			
			#must not have more then 1 restricted card
			restrict = reduce(self._restricted, acc_deck.keys(), [])
			if len(restrict) > 1:
				raise InvalidDeckException("Invalid Deck.  Deck Loaded by {} has too many restricted cards. {}.".format(octgn.me, str(restrict)))
				
			#must not have any banned cards
			banned = reduce(self._banned, acc_deck.keys(), [])
			if len(banned) > 0:
				raise InvalidDeckException("Invalid Deck.  Deck Loaded by {} has a banned card. {}.".format(octgn.me, str(restrict)))

				
			#shuffle the deck for good measure
			octgn.me.deck.shuffle()
		
		return True
	
	def _addMarker(self, octgn, card, marker):
		if card._id in { c._id: c for c in octgn.table}.keys():
			if marker not in card.markers:
				card.markers[marker] = 1
			else:
				card.markers[marker] += 1
	def _removeMarker(self, octgn, card, marker):
		if card._id in { c._id: c for c in octgn.table}.keys():
			card.markers[marker] -= 1
		if card.markers[marker] <= 0:
			del card.markers[marker]
	
	@log_calls()
	@validate(['octgn', 'card'])
	def addWound(self, card=None, octgn=None, *args, **kwargs):
		self._addMarker(octgn, card, self._markerWound)
			
	@log_calls()
	@validate(['octgn', 'card'])
	def removeWound(self, card=None, octgn=None, *args, **kwargs):
		self._removeMarker(octgn, card, self._markerWound)

	@log_calls()
	@validate(['octgn', 'card'])
	def addSuccess(self, card=None, octgn=None, *args, **kwargs):
		self._addMarker(octgn, card, self._markerSuccess)
			
	@log_calls()
	@validate(['octgn', 'card'])
	def removeSuccess(self, card=None, octgn=None, *args, **kwargs):
		self._removeMarker(octgn, card, self._markerSuccess)
		