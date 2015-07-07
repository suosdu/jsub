'''
Created on 2015-06-24 11:45:28

@author: suo
'''
import sys
from subprocess import call

siteName = sys.argv[1]

call(['python','tmsg.py','Determine which mirror DB to use'])

if siteName in ['CLOUD.IHEP-OPENSTACK.cn', 'CLOUD.IHEP-OPENNEBULA.cn']:
    call(['sed','-i',"'s/202.114.78.211/202.122.37.75/g'",'simu.macro'])
    print 'Use site local DB 202.122.37.75'
else:
    print 'Use default DB 202.114.78.211'