'''
Created on 2015-06-30 22:26:30

@author: suo
'''
from DIRAC.Core.Base import Script
print "hello00"
#Script.initialize()
Script.parseCommandLine( ignoreErrors = False )
print "hello"
from backend.Backend import Backend
from DIRAC.Interfaces.API.Dirac import Dirac as GridDirac
from DIRAC.Interfaces.API.Job import Job
from DIRAC.Core.Security.ProxyInfo import getProxyInfo
from utility.ResolvePath import trimJoinPathElement
class Dirac(Backend):
    def __init__(self, backendDict = None):
        if backendDict!=None:
            self.site = backendDict['Site']
            self.jobGroup = backendDict['JobGroup']
            self.outputSE = backendDict['OutputSe']
            self.outputDir = trimJoinPathElement(backendDict['OutputDir'])
            if 'OutputPath' in backendDict:
                self.outputPath = backendDict['OutputPath']
            else:
                self.outputPath = ''
        else:
            self.site = ''
            self.jobGroup = ''
            self.outputSE = ''
            self.outputDir = ''
            self.outputPath = ''
    
    def getDFCprefix(self):
        username = getProxyInfo()['Value']['username']
        initial = username[0]
        prefix = '/cepc/user/' + initial + '/' + username# + '/' 
        return prefix
    
    def submit(self, param):        
        j = Job()
        j.setName(param['jobName'])
        j.setExecutable(param['jobScript'],logFile = param['jobScriptLog'])
        if self.site:
            j.setDestination(self.site)
        if self.jobGroup:
            j.setJobGroup(self.jobGroup)            
        j.setInputSandbox(param['inputSandbox'])
        j.setOutputSandbox(param['outputSandbox'])
        j.setOutputData(param['outputData'], outputSE = self.outputSE, outputPath = self.outputPath)

        dirac = GridDirac()
        result = dirac.submit(j)

        status = {}
        status['submit'] = result['OK']
        if status['submit']:
            status['job_id'] = result['Value']

        return status

    def setSite(self, site):
        self.site = site
        
    def setJobGroup(self, group):
        self.jobGroup = group

    def setOutputSE(self,se):
        self.outputSE = se
        
    def setOutputPath(self,path):
        self.outputPath = path


