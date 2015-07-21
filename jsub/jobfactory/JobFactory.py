#coding:utf-8
'''
Created on 2015-07-03 14:40:28

@author: suo
'''
import os,copy
from utility.Workspace import createMasterRepoDir
from utility.UserConf import repo_path

class JobFactory(object):
    
    def __init__(self):
        self.properties = {'inputSandbox':{},'outputSandbox':{}}
    
    def createSubJobs(self,experiment,splitter,backend,stepNumList):
        masterDir = createMasterRepoDir(repo_path)
        count = 1
        subjobs = []
        jobParam = {'jobScriptLog':'script.log',
                    'inputSandbox':[],
                    'outputSandbox':['script.log','job.log','job.err'],
                    'outputData':[],
                    'masterDir': masterDir}
        #outputsandbox可以统一处理
        if '1' in stepNumList:
            jobParam['outputSandbox'].extend(self.properties['outputSandbox']['sim'])
        if '2' in stepNumList:
            jobParam['outputSandbox'].extend(self.properties['outputSandbox']['rec'])
#         if '3' in stepNumList:
#             jobParam['outputSandbox'].extend(self.properties['outputSandbox']['ana'])

        splitResult = splitter.split()
        totalJobs = len(splitResult)
        jobParam['totalJobs'] = totalJobs 
           
        for each in splitResult:
            currentjobParam = copy.deepcopy(jobParam)
            for key in each:
                currentjobParam[key] = each[key]

            currentjobParam['subDir'] = os.path.join(masterDir,str(count))
            os.mkdir(currentjobParam['subDir'])

            currentjobParam['jobName'] = "%s_v1_%s_%s"%(experiment,os.path.basename(masterDir),str(count))
            currentjobParam['jobScript'] = os.path.join(currentjobParam['subDir'],'runtimeScript.py')
            currentjobParam['inputSandbox'].append(currentjobParam['jobScript'])

            self.setSpecialParam(currentjobParam, backend, stepNumList)
            
            subjobs.append(currentjobParam)
            count+=1

        return subjobs
    
    def setSpecialParam(self,jobParam,backend,stepNumList):
        raise NotImplementedError           
