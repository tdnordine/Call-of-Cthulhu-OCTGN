import inspect

class OCTGNPatcher(object):
	def __init__(self, scope):
		for handler in inspect.getmembers(self, inspect.ismethod):
			if hasattr(handler[1], "_is_event_handler"):
				scope[handler[0]] = getattr(self, handler[0])

	@classmethod
	def EventHandler(cls, func):
		func._is_event_handler = True
		return func	