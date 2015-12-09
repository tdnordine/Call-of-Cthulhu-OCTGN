

class DomainCollection(object):

	resdict = {
		'Resource:Cthulhu':						("Cthulhu Resource", "a5173cd9-bafe-4be2-ae6f-11464f7260cf"),
		'Resource:Hastur':						("Hastur Resource", "3911052d-c25b-471d-92af-8aae4a18cce1"),
		'Resource:Shub-Niggurath':				("Shub-Niggurath Resource", "c9e080cd-fa2e-4397-a054-031945af4d8e"),
		'Resource:Yog-Sothoth':					("Yog-Sothoth Resource", "807d0966-15d7-4e45-88b3-87c77fc25288"),
		'Resource:The Agency':					("Agency Resource", "590456bb-17bc-4831-a08c-380def83486f"),
		'Resource:Miskatonic University':			("Miskatonic Resource", "93ec59f4-0a91-43bc-92da-210a16f20274"),
		'Resource:The Syndicate':					("Syndicate Resource", "d5ff5bee-09cc-44bb-b78c-c1c19b586028"),
		'Resource:The Order of the Silver Twilight':	("Silver Twilight Resource", "f5cfe322-21a4-4427-91ff-cd5b880c5848"),
		'Resource:Neutral':						("Neutral Resource", "e6d100e4-f79b-4b91-9853-16974ea47fb0"),
		'Resource:Zoog':						("Zoog Resource", "94dc59b3-409e-419d-be97-cb4877cdd507")
	}

	domainKeys = ['Domain 1','Domain 2','Domain 3', 'SpareDom 1', 'SpareDom 2', 'SpareDom 3', 'SpareDom 4', 'SpareDom 5']
	
	domainPositions = [	
		("f22ee55c-8f47-4174-a7a4-985731a74d30",-528,20),
		("a8cec1b8-1121-4612-80c4-c66a437cc2e0",-528,94),
		("d8a151e4-28c8-4653-b826-ebda237b776b",-528,168),
		('None',-528,242),
		('None',-668,20),
		('None',-668,94),
		('None',-668,168),
		('None',-668,242)
	]
	
	def __init__(self, domains=None):
		if domains is None:
			domains = []
		
		self.domains = [DomainInfo(*d) for d in map(None, self.domainKeys, self.domainPositions, domains)]
		
	def __len__(self):
		return len([d for d in self.domains if d.Domain is not None])

class DomainInfo(object):
	def __init__(self, keyName, position, domain=None):
		self.keyName = keyName
		self.position = position
		self.domain = domain
		
		
class Domain(object):
	def __init__(self):
		self.resources = []
		