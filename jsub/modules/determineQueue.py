'''
Created on 2015-06-30 17:36:47

@author: suo
'''
import random,os,sys
from subprocess import call

siteName = sys.argv[1]
max_q_time = sys.argv[2]

if siteName.startswith('CLOUD'):
    max_q_time = 0
if max_q_time != 0:
    q_time = max_q_time * random.random()
    q_msg = 'Queue for %.2f seconds' %q_time
    tmsg(q_msg)
    setJobStatus(q_msg)
    q_cmd = 'sleep %f' %q_time
    os.system(q_cmd)
    tmsg('End queue.')