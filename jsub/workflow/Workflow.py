'''
Created on 2015-05-27 11:43:10

@author: suo
'''
import os,copy
from utility.Compress import tarDir

class Workflow(object):
    
    def __init__(self):
        self.jobSteps = []
        self.stepNumList = []
        self.jobParam = {}
        
    def updateForSubjob(self,jobParam):
        self.jobParam = copy.deepcopy(jobParam)
        
    def prepare(self,f):
        raise NotImplementedError

    def download(self,f):
        raise NotImplementedError
        
    def executeSteps(self,f):
        raise NotImplementedError
    
    def uploadData(self,f):
        raise NotImplementedError
        
    def complete(self,f):
        raise NotImplementedError
    
    def generateScript(self):
        try:
            with open(os.path.join(self.jobParam['subDir'],'runtimeScript.py'),'w') as f:
                self.prepare(f)
                self.download(f)
                self.executeSteps(f)
                self.uploadData(f)
                self.complete(f)
        except IOError as err:
            print 'IOError ',str(err)
        rootDir =  os.path.dirname(os.getcwd())               
        tarDir(os.path.join(rootDir,'modules/') ,os.path.join(self.jobParam['subDir'],'modules.tgz'))

        