import wrapt


# decorators
def register(name, evts):
	def _register(wrapped):
		evts.registerHandler(name, wrapped)
		return wrapped
	return _register


def validate(parms=[]):
	@wrapt.decorator
	def _validator(wrapped, instance, pargs, kwargs):
		for p in parms:
			psplit = p.split('=', 1)
			if len(psplit) == 1:
				parm = psplit[0]
				
				if parm not in kwargs or kwargs[parm] is None:
					raise ValueError("{}: {} doesn't exist or is None.".format(wrapped.__name__, parm))
			
			else:
				parm = psplit[0]
				val = psplit[1]
				
				if parm not in kwargs or kwargs[parm] != val:
					raise ValueError("{}: {} doesn't exist or is not {}.".format(wrapped.__name__, parm, val))
		
				
		return wrapped(*pargs, **kwargs)
	return _validator


@wrapt.decorator	
def isMe(wrapped, instance, pargs, kwargs):
	if 'octgn' not in kwargs or 'player' not in kwargs:
		raise ValueError("")
		
	octgn = kwargs['octgn']
	player = kwargs['player']
	if octgn.me != player:
		raise ValueError("IsMe Failed because it wasn't me.")
	return wrapped(*pargs, **kwargs)

@wrapt.decorator	
def isMine(wrapped, instance, pargs, kwargs):
	if 'octgn' not in kwargs: 
		raise ValueError("No octgn defined.")
		
	if 'player' not in kwargs and 'card' not in kwargs and 'cardgroup' not in kwargs and 'groups' not in kwargs:
		raise ValueError("No possible owner defined.")
	
	if 'player' in kwargs:
		player = kwargs['player']
	elif 'card' in kwargs:
		player = kwargs['card'].owner
	elif 'cardgroup' in kwargs:
		player = kwargs['cardgroup'].player
	elif 'groups' in kwargs:
		player = kwargs['groups'][0].player
		
	if player is None:
		raise ValueError("No Player object available.")
		
	octgn = kwargs['octgn']
	if octgn.me != player:
		raise ValueError("IsMine Failed because it isn't Mine.{} and {}.".format(octgn.me, player))
	return wrapped(*pargs, **kwargs)	
	
@wrapt.decorator
def isNotMe(wrapped, instance, pargs, kwargs):
	if 'octgn' not in kwargs or 'player' not in kwargs:
		raise ValueError("")
		
	octgn = kwargs['octgn']
	player = kwargs['player']
	if octgn.me == player:
		raise ValueError("IsNotMe Failed because it was me.")		
	return wrapped(*pargs, **kwargs)

