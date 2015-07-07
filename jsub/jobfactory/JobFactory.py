'''
Created on 2015-07-03 14:40:28

@author: suo
'''
import os
from utility.Workspace import createMasterRepoDir
from utility.UserConf import repo_path

class JobFactory(object):
    
    def __init__(self):
        self.properties = {'inputSandbox':{},'outputSandbox':{}}
        self.stepNumList = []
    
    def createSubJobs(self,experiment,splitter,backend):
        masterDir = createMasterRepoDir(repo_path)
        count = 1
        subjobs = []
        jobParam = {'jobScriptLog':'script.log',
                    'inputSandbox':[],
                    'outputSandbox':['script.log','job.log','job.err'],
                    'outputData':[],
                    'masterDir': masterDir}
        #outputsandbox可以统一处理
        if '1' in self.stepNumList:
            jobParam['outputSandbox'].extend(self.properties['outputSandbox']['sim'])
        if '2' in self.stepNumList:
            jobParam['outputSandbox'].extend(self.properties['outputSandbox']['rec'])
#         if '3' in self.stepNumList:
#             jobParam['outputSandbox'].extend(self.properties['outputSandbox']['ana'])
            
        for each in splitter.split():
            for key in each:
                jobParam[key] = each[key]
            jobParam['jobScript'] = os.path.join(jobParam['subDir'],'runtimeScript.py')
            jobParam['inputSandbox'].append(jobParam['jobScript'])
            jobParam['jobName'] = "%s_v1_%s_%s"%(experiment,masterDir,str(count))
            jobParam['subDir'] = os.path.join(masterDir,str(count))
            
            self.setSpecialParam(jobParam, backend)
            
            subjobs.append(jobParam)
            count+=1

        return subjobs
    
    def setSpecialParam(self,jobParam):
        raise NotImplementedError           