#from DIRAC.Core.Base import Script
#Script.parseCommandLine( ignoreErrors = False )

from Dirac import Dirac
from pprint import pprint

dirac = Dirac()
pprint( dirac.getDFCprefix())
