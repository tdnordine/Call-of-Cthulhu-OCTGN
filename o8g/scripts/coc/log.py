import logging
import wrapt

class OctgnLogHandler(logging.Handler):
	def __init__(self, octgn=None, whisper=None):
		logging.Handler.__init__(self)
		self.whisper = octgn.whisper if octgn is not None else whisper
		
		if self.whisper is None:
			self.whisper = lambda x: x
		
		self.backlog = []
	
	def emit(self, record):
		try:
			while len(self.backlog) > 0:
				r = self.backlog[0]
				self._emit(r.msg)
				del self.backlog[0]
				
			self._emit(record.msg)
		except:
			self.backlog.append(record)
	
	def _emit(self, msg):
		self.whisper(msg)
		

def log_calls(logger=logging.getLogger("coc.enterexit")):
	@wrapt.decorator
	def _log_calls(wrapped, instance, args, kwargs):
		logger.debug('entering {}.'.format(wrapped.__name__))
		try:
			return wrapped(*args, **kwargs)
		finally:
			logger.debug('exiting {}'.format(wrapped.__name__))
		
	return _log_calls