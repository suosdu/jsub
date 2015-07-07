'''
Created on 2015-07-06 15:42:47

@author: suo
'''
import os
from jobfactory.JobFactory import JobFactory

class CepcJobFactory(JobFactory):
    
    def __init__(self):
        super(CepcJobFactory, self).__init__()
        self.properties['inputSandbox']['sim'] = ['simu.macro','event.macro']
        self.properties['inputSandbox']['rec'] = ['PandoraSettingsDefault.xml','PandoraLikelihoodData9EBin.xml','reco.xml']
        
        self.properties['outputSandbox']['sim'] = ['simu.macro','simu.sh','simu.log']
        self.properties['outputSandbox']['rec'] = ['reco.sh','reco.log']

                
    def setSpecialParam(self, jobParam, backend):
        jobParam['se'] = backend.outputSE
        jobParam['inputSandbox'].append('LFN:/cepc/lustre-ro'+jobParam['inputFilePath'])
        jobParam['inputSandbox'].append(os.path.join(self.jobParam['subDir'],'modules.tgz'))
        if '1' in self.stepNumList:
            jobParam['inputSandbox'].extend([os.path.join(jobParam['subDir'],each) for each in self.properties['inputSandbox']['sim']])
            jobParam['outputData'].append('LFN:'+os.path.join(backend.getDFCprefix(),backend.outputDir,'sim',os.path.splitext(jobParam['inputFileName'])[0]+'_sim.slcio'))
        if '2' in self.stepNumList:
            jobParam['inputSandbox'].extend([os.path.join(jobParam['master'],each) for each in ['PandoraSettingsDefault.xml','PandoraLikelihoodData9EBin.xml']])
            jobParam['inputSandbox'].append(os.path.join(jobParam['subDir'],'reco.xml'))
            jobParam['outputData'].append('LFN:'+os.path.join(backend.getDFCprefix(),backend.outputDir,'rec',os.path.splitext(jobParam['inputFileName'])[0]+'_rec.slcio'))
