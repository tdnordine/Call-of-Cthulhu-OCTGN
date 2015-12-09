import unittest
import mock
from coc.decorators import isMe, isNotMe, isMine, validate

class DecoratorTests(unittest.TestCase):
	def setUp(self):
		pass
		
		
	def test_isMe(self):
		m = mock.Mock()
		octgn = mock.Mock()
		player = mock.Mock()
		octgn.configure_mock( **{'me' : player})
		im = isMe(m)
		
		im( **{'octgn':octgn, 'player':player})
		
		self.assertTrue(m.called)

	def test_isMe_WithNotMe(self):
		m = mock.Mock()
		octgn = mock.Mock()
		player = mock.Mock()
		octgn.configure_mock( **{'me' : mock.Mock()})
		im = isMe(m)

		self.assertRaises(ValueError, im, octgn=octgn, player=player)		
		self.assertFalse(m.called)


	def test_isMe_WithNoPlayer(self):
		m = mock.Mock()
		octgn = mock.Mock()
		octgn.configure_mock( **{'me' : mock.Mock()})
		im = isMe(m)

		self.assertRaises(ValueError, im, octgn=octgn)		
				
		self.assertFalse(m.called)

		
	def test_isNotMe(self):
		m = mock.Mock()
		octgn = mock.Mock()
		player = mock.Mock()
		octgn.configure_mock( **{'me' : mock.Mock()})
		im = isNotMe(m)
		
		im( **{'octgn':octgn, 'player':player})
		
		self.assertTrue(m.called)

	def test_isNotMe_WithMe(self):
		m = mock.Mock()
		octgn = mock.Mock()
		player = mock.Mock()
		octgn.configure_mock( **{'me' : player})
		im = isNotMe(m)
		
		self.assertRaises(ValueError, im, octgn=octgn, player=player)				
		self.assertFalse(m.called)

		
	def test_isMine_Card(self):
		m = mock.Mock()
		player = mock.Mock()
		octgn = mock.Mock()
		card = mock.Mock()
		card.configure_mock( **{'owner': player})
		octgn.configure_mock( **{'me' : player})
		im = isMine(m)
		
		im( **{'octgn':octgn, 'card' : card})
		
		self.assertTrue(m.called)		

	def test_isMine_Card_WithNotMe(self):
		m = mock.Mock()
		player = mock.Mock()
		octgn = mock.Mock()
		card = mock.Mock()
		card.configure_mock( **{'owner': player})
		octgn.configure_mock( **{'me' : mock.Mock()})
		im = isMe(m)

		self.assertRaises(ValueError, im, octgn=octgn, card=card)		
		self.assertFalse(m.called)
		
	def test_isMine_CardGroup(self):
		m = mock.Mock()
		player = mock.Mock()
		octgn = mock.Mock()
		cardgroup = mock.Mock()
		cardgroup.configure_mock( **{'player': player})
		octgn.configure_mock( **{'me' : player})
		im = isMine(m)
		
		im( **{'octgn':octgn, 'cardgroup' : cardgroup})
		
		self.assertTrue(m.called)		

	def test_isMine_CardGroup_WithNotMe(self):
		m = mock.Mock()
		player = mock.Mock()
		octgn = mock.Mock()
		cardgroup = mock.Mock()
		cardgroup.configure_mock( **{'player': player})
		octgn.configure_mock( **{'me' : mock.Mock()})
		im = isMe(m)

		self.assertRaises(ValueError, im, octgn=octgn, cardgroup=cardgroup)		
		self.assertFalse(m.called)
		
	def test_isMine_Groups(self):
		m = mock.Mock()
		player = mock.Mock()
		octgn = mock.Mock()
		groups = [mock.Mock() for i in range(0, 3)]
		for g in groups:
			g.configure_mock( **{'player': player})
		octgn.configure_mock( **{'me' : player})
		im = isMine(m)
		
		im( **{'octgn':octgn, 'groups' : groups})
		
		self.assertTrue(m.called)		

	def test_isMine_Groups_WithNotMe(self):
		m = mock.Mock()
		player = mock.Mock()
		octgn = mock.Mock()
		groups = [mock.Mock() for i in range(0, 3)]
		for g in groups:
			g.configure_mock( **{'player': player})
		octgn.configure_mock( **{'me' : mock.Mock()})
		im = isMe(m)

		self.assertRaises(ValueError, im, octgn=octgn, groups=groups)		
		self.assertFalse(m.called)		
		
	def test_validateParamExists(self):
		v = validate(['param1'])
		m = mock.Mock()
		m.configure_mock( **{'__name__':"testfunc"})
		_v = v(m)
		
		_v(param1="test")

		self.assertTrue(m.called)

	def test_validateParamDoesntExists(self):
		v = validate(['param1'])
		m = mock.Mock()
		m.configure_mock( **{'__name__':"testfunc"})
		_v = v(m)
		
		self.assertRaises(ValueError, _v, paramX="test")

		self.assertFalse(m.called)
		

		
	def test_validateParamValue(self):
		v = validate(['param1=test'])
		m = mock.Mock()
		m.configure_mock( **{'__name__':"testfunc"})
		_v = v(m)
		
		_v(param1="test")
		
		self.assertTrue(m.called)
		
	def test_validateParamNotCorrectValue(self):
		v = validate(['param1=testx'])
		m = mock.Mock()
		m.configure_mock( **{'__name__':"testfunc"})
		_v = v(m)
		
		self.assertRaises(ValueError, _v, param1="test")
		
		self.assertFalse(m.called)
