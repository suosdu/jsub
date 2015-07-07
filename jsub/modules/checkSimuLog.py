'''
Created on 2015-06-25 12:54:49

@author: suo
'''
import sys
from subprocess import call

if sys.argv[1]!=0:
    if call(['grep','Database connection failed', 'simu.log'])!=0:
        call(['python','setJobStatus.py','CEPC_Script','DB connection failed'])
        sys.exit(21)
    call(['python','setJobStatus.py','CEPC_Script','Simulation Error'])
    sys.exit(20)