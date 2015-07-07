'''
created on 2015-01-08 14:46:24

@author: SUO Bing
'''

import os
import ConfigParser

cf = ConfigParser.ConfigParser()
repo_path = ''
try:
    cf.read(os.path.expanduser('~/.jsubrc'))
#     o = cf.options('Configuration')
#     print "Configuration: ",o
    repo_path = cf.get('Configuration', 'repository_dir')
    print "repository_dir: ",repo_path
except IOError as err:
    print str(err)
    
