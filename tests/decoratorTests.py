import unittest
import mock
import events

class decoratorTests(unittest.TestCase):
		
	def test_isMeDecorator(self):
		me = mock.Mock()	
		args = mock.Mock()
		args.player = me
		
		inner = mock.Mock()
		print inner
		print events.isMe
		print events.isMe(None)
		func = events.isMe(inner)
		print func
		
		func(args)
		
		inner.assert_called_with(args)
		
if __name__ == '__main__':
	unittest.main()