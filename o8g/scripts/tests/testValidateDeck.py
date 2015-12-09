import unittest
import mock
from coc.cards import CardActionHandler, InvalidDeckException
import xml.etree.ElementTree as et

class DeckValidationTests(unittest.TestCase):
		
	def setUp(self):
		deck_text = '''<?xml version="1.0" encoding="utf-8" standalone="yes"?>
			<deck game="43054c18-2362-43e0-a434-72f8d0e8477c" sleeveid="0">
			<section name="Draw Deck" shared="False">
				<card qty="3" id="862c8edf-c273-4b3d-a9a9-cb222085092d">Crooked Cop</card>
				<card qty="3" id="85cdbb92-09d8-4d86-9fe0-5e9c43946544">Obsessive Detective</card>
				<card qty="3" id="1a750452-8821-41ba-96be-d6a1e1872097">Obsessive Inmate</card>
				<card qty="2" id="cb3bec6a-8e46-4d1e-a46f-db4b52dba092">Ol' Lazy Eyes</card>
				<card qty="3" id="5e6ed754-a71f-4e30-a133-84e0ce13ab09">Peerless Tracker</card>
				<card qty="3" id="45f006f4-02ed-4b8d-b095-eb5efe58d087">Performance Artist</card>
				<card qty="2" id="5da1fd9d-7244-428d-bca7-79bc5c93a3e7">Prepared Alienist</card>
				<card qty="3" id="e27b1b8d-6fac-41b0-b88b-cdff5cdab190">Relentless Stalker</card>
				<card qty="3" id="b0ab377e-913e-4e7e-a1bf-11c8d423be62">Trial Judge</card>
				<card qty="2" id="45f006f4-02ed-4b8d-b095-eb5efe58d082">* Victoria Glasser</card>
				<card qty="3" id="fe26b1c0-8f1d-4452-b234-3902c1747078">* Guardian Pillar</card>
				<card qty="3" id="af4154b4-9d08-451f-8c1b-41fa4a9af06f">* San Marco Basilica</card>
				<card qty="2" id="fe26b1c0-8f1d-4452-b234-3902c1747049">* The Cavern of Flame</card>
				<card qty="3" id="fe26b1c0-8f1d-4452-b234-3902c1747030">* The Seventy Steps</card>
				<card qty="3" id="f26280d4-6260-4475-9f94-e496394af076">Apeirophobia</card>
				<card qty="3" id="fe26b1c0-8f1d-4452-b234-3902c1747082">_Behind Bars</card>
				<card qty="3" id="35eaac48-c517-49d7-84e0-f1260de77c46">Unending Festivities</card>
			</section>
		</deck>'''
		
		self.deck = self._load_cards(deck_text)
				
	def _load_cards(self, cards_as_string):	
		cardlist = []
		deck = et.fromstring(cards_as_string)
		for card in deck.iter('card'):
			for c in range(int(card.attrib['qty'])):
				cardlist.append( self._create_mock_card(card.text))	
				
		return cardlist
		
	def _create_mock_card(self, name):
		m = mock.Mock()
		m.configure_mock( **{'name':name})
		return m
	
	def _configure_mock_for_validation(self, new_deck):
		octgn = mock.Mock()

		octgn.mute = mock.MagicMock()
		octgn.me = player = mock.Mock()
		octgn.me.deck = mock.MagicMock()
		octgn.me.deck.__iter__.return_value = new_deck
		octgn.me.deck.__len__.return_value = len(new_deck)
		octgn.me.piles = mock.MagicMock(spec_set=dict)
		octgn.me.piles.__getitem__.return_value = octgn.me.deck

		group = mock.MagicMock()
		groups = mock.MagicMock(spec_set=list)
		groups.__iter__.return_value = iter([group])
		groups.__getitem__.return_value = group 
		
		group.player = player

		return (octgn, groups)
		
	def test_LessThen50(self):
		cah = CardActionHandler(mock.Mock())
		
		new_deck = self.deck
		octgn, groups = self._configure_mock_for_validation(new_deck)
		
		self.assertRaises(InvalidDeckException, cah.validateDeck, octgn=octgn, groups=groups)
			
			
	def test_ValidDeck(self):
		cah = CardActionHandler(mock.Mock())

		extra_cards = self._load_cards('''<card qty="3" id="ff1087a7-9c94-463e-8359-8e0483f99e05">Beneath the Burning Sun</card>''')
		
		new_deck = self.deck + extra_cards
		octgn, groups = self._configure_mock_for_validation(new_deck)
		
		self.assertTrue(cah.validateDeck(**{'octgn':octgn, 'groups':groups}))
		
		
	def test_TooManyOfOne(self):
		cah = CardActionHandler(mock.Mock())
		extra_cards = self._load_cards('''<deck><card qty="2" id="cb3bec6a-8e46-4d1e-a46f-db4b52dba092">Ol' Lazy Eyes</card>
			<card qty="1" id="5da1fd9d-7244-428d-bca7-79bc5c93a3e7">Prepared Alienist</card>
			</deck>
		''')
		
		new_deck = self.deck + extra_cards
		octgn, groups = self._configure_mock_for_validation(new_deck)

		self.assertRaises(InvalidDeckException, cah.validateDeck, octgn=octgn, groups=groups)
			
			
	def test_TooManyRestricted(self):
		cah = CardActionHandler(mock.Mock())
		extra_cards = self._load_cards('''<card qty="3" id="1a750452-8821-41ba-96be-d6a1e1872051">* Infernal Obsession</card>''')

		new_deck = self.deck + extra_cards
		octgn, groups = self._configure_mock_for_validation(new_deck)
		
		self.assertRaises(InvalidDeckException, cah.validateDeck, octgn=octgn, groups=groups)
