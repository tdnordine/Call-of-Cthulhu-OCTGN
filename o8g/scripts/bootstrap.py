import sys
sys.path.append( wd("scripts") )
sys.path.append( wd("scripts\\lib") )

import logging
from coc.octgn import Octgn
from coc.log import OctgnLogHandler
from coc.player import PlayerActionHandler
from coc.cards import CardActionHandler
from coc.domain import DomainCollection

coc_logger = logging.getLogger("coc")
coc_logger.setLevel(logging.DEBUG)
coc_logger.addHandler(OctgnLogHandler(whisper=whisper))

enter_logger = logging.getLogger("coc.enterexit")
enter_logger.setLevel(logging.DEBUG)
enter_logger.addHandler(OctgnLogHandler(whisper=whisper))

coc_logger.debug("Creating Base Objects.")
octgn = Octgn(globals(), domains=DomainCollection())

pah = PlayerActionHandler(octgn)
cah = CardActionHandler(octgn)

coc_logger.debug("Everything is setup and good to go!")