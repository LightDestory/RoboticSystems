#
#
#

import sys

from pathlib import Path
CURRENT_POSITION = Path(__file__).parent
sys.path.append(f"{CURRENT_POSITION}/../../")

from lib.phidias.Types import *
from lib.phidias.Main import *
from lib.phidias.Lib import *
from lib.phidias.Agent import *

# beliefs interpreted by the robot
class go_to(Belief): pass
class target_reached(Reactor): pass

class go(Procedure): pass

def_vars('X', 'Y', 'F')

# ---------------------------------------------------------------------
# Agent 'main'
# ---------------------------------------------------------------------
class main(Agent):
    def main(self):
        # commands
        go(X,Y) >> [ +go_to(X,Y)[{'to': 'robot@127.0.0.1:6566'}] ]
        +target_reached()[{'from':F}] >> [ show_line("Target reached") ]


ag = main()
ag.start()
PHIDIAS.run_net(globals(), 'http')
PHIDIAS.shell(globals())

