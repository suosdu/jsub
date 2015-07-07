'''
Created on 2015-07-06 15:44:46

@author: suo
'''
import os
from base.JobFactory import JobFactory

class BesJobFactory(JobFactory):
    
    def __init__(self):
        super(BesJobFactory, self).__init__()
        #####for bes###
        self.properties['outputSandbox']['sim'] = ['bosslog', 'bosserr']
        self.properties['outputSandbox']['rec'] = ['rantrg.log', 'rantrg.err','recbosslog', 'recbosserr']
        
    def setSpecialParam(self, jobParam):
        JobFactory.setSpecialParam(self, jobParam) 