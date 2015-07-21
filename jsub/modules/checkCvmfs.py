#coding:utf-8
'''
Created on 2015-05-19 22:23:57

@author: suo
'''
import os,sys
from subprocess import call

cvmfsPath = sys.argv[1]
jobID = sys.argv[2]
#--------------------------------------------------------------------------   
'''version Yan'''
call(['python','tmsg.py','Check cvmfs'])

for repeatTimes in range(10):
    found_cvmfs = not call(['ls',cvmfsPath])#找到的话,found_cvmfs == 1
    if found_cvmfs:
        break
    else:
        call(['sleep','5'])
if not found_cvmfs:
    call(['python','setJobStatus.py',jobID,'CEPC_script','cvmfs not found'])
    sys.exit(11)
