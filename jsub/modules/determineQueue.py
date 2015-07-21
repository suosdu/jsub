'''
Created on 2015-06-30 17:36:47

@author: suo
'''
import random,os,sys
from subprocess import call

siteName = sys.argv[1]
max_q_time = int(sys.argv[2])
jobID = sys.argv[3]
description = sys.argv[4]

if siteName.startswith('CLOUD'):
    max_q_time = 0
if max_q_time != 0:
    q_time = max_q_time * random.random()
    q_msg = 'Queue for %.2f seconds' %q_time
    call(['python','tmsg.py',q_msg])
    call(['python','setJobStatus.py',jobID,description,q_msg])
    call(['sleep','%f'%q_time])
    call(['python','tmsg.py','End queue'])
