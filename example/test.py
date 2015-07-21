import sys
sys.path.append('/home/cc/suob/jsub/jsub')

from backend.Dirac import Dirac

d = Dirac()

print d.getDFCprefix()
