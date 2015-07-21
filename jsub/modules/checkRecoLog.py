'''
Created on 2015-06-25 12:26:46

@author: suo
'''
import sys
from subprocess import call

sInfo = 'MyLCIOOutputProcessor: %s events in 1 runs written to file' % sys.argv[1]
jobID = sys.argv[2]
try:
    with open('reco.log') as recoLog:
        recoLogfind = False
        for line in recoLog:
            if line.find(sInfo) != -1:
                recoLogfind = True
                break
        if not recoLogfind:
            call(['python','setJobStatus.py',jobID,'CEPC_script','Reconstruction Error'])
            sys.exit(30)
except IOError as err:
    print 'IOError ',str(err)
