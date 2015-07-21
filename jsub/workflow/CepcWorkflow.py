'''
Created on 2015-06-24 11:03:54

@author: suo
'''
from workflow.Workflow import Workflow

class CepcWorkflow(Workflow):
    
    def __init__(self):
        super(CepcWorkflow,self).__init__()
    
    def prepare(self, f):
        content = '''#!/usr/bin/env python
import sys,os,tarfile
from subprocess import call
from DIRAC import siteName
from DIRAC.Core.Base import Script
Script.parseCommandLine( ignoreErrors = False )

\'''********************Preparation********************\'''
jobID = os.environ.get('DIRACJOBID', '0')
siteName = siteName()

call(['python','setJobStatus.py',jobID,'CEPC_script','Preparation'])

tarobj = tarfile.open('modules.tgz', "r:gz")
tarobj.extractall()
tarobj.close()

call(['python','checkExeEnv.py'])

result = call(['python','checkCvmfs.py','%s',jobID])
if result!=0:
    sys.exit(result)

call(['python','listInputSandbox.py'])

call(['python','determineMirrorDB.py',siteName])\n''' % '/cvmfs/cepc.ihep.ac.cn/'

        if self.jobParam['totalJobs'] < 50 or self.jobParam['eventNum'] < 30:
            timeString = 'max_q_time = 0\n'
        elif self.jobParam['eventNum'] < 60:
            timeString = 'max_q_time = 60 * 5\n'
        elif self.jobParam['eventNum'] < 120:
            timeString = 'max_q_time = 60 * 10\n'
        else:
            timeString = 'max_q_time = 60 * 15\n'
        
        content= content+timeString+'''call(['python','determineQueue.py',siteName,str(max_q_time),jobID,'CEPC_script'])\n'''
        f.write(content)

    def download(self,f):
        pass
    
    def executeSteps(self, f):
        if '1' in self.stepNumList:
            sim = self.jobSteps[self.stepNumList.index('1')]
            content = '''\n\'''********************Execute Simulation********************\'''
call(['python','tmsg.py','Generate shell script for simulation'])
call(['chmod','755','simu.sh'])
call(['python','setJobStatus.py',jobID,'CEPC_script','%s Simulation'])
call(['python','tmsg.py','Start simulation'])
result = call(['./simu.sh','%s'])

call(['python','checkSimuLog.py',str(result),jobID])\n''' % (sim.executable,sim.executable)
            f.write(content)
            
        if '2' in self.stepNumList:
            rec = self.jobSteps[self.stepNumList.index('2')]
            content = '''\n\'''********************Execute Reconstruction********************\'''
call(['python','tmsg.py','Generate shell script for reconstruction'])
call(['chmod','755','reco.sh'])
call(['python','setJobStatus.py',jobID,'CEPC_script','%s Reconstruction'])
call(['python','tmsg.py','Start reconstruction'])
call(['./reco.sh','%s'])

call(['python','checkRecoLog.py','%s',jobID])\n''' % (rec.executable,rec.executable,self.jobParam['eventNum'])
            f.write(content)
    
    def uploadData(self,f):
        content = '''\n\'''********************Upload Data********************\'''
from uploadData import uploadData
lfns = %s
se = '%s\''''% (self.jobParam['outputData'], self.jobParam['se'])

        content+='''
for lfn in lfns:
    call(['python','setJobStatus.py',jobID,'CEPC_script','Uploading Data'])
    result = uploadData(lfn, se)
    if not result['OK']:
        try:
            with open ('job.err','a') as errFile:
                print>>errFile, 'Upload Data Error:\\n%s' % result
        except IOError as e:
            print 'IOError:',str(e)\n'''
        f.write(content)        
    
    def complete(self,f):
        content ='''\n\'''********************Job Completed********************\'''
call(['python','tmsg.py','Job Completed. Files in current dir:'])
call(['ls','-l'])
call(['python','setJobStatus.py',jobID,'CEPC_script','Done'])
call(['python','tmsg.py','Job Done'])\n'''
        f.write(content)
                     
if __name__ == '__main__':
    import os
    w  = CepcWorkflow()
    w.stepNumList = ['1','2']
    w.jobPara = {'totalJobs':50,'evtmax':30}
    w.scriptpath = os.path.join(os.getcwd(),'maintest.py')
    w.generateScript()
