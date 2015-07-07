'''
Created on 2015-05-19 21:45:37

@author: suo
'''
import sys
from DIRAC.WorkloadManagementSystem.Client.JobReport import JobReport

jobID = sys.argv[1]
experiment = sys.argv[2]
message = sys.argv[3]

jobReport = JobReport(int(jobID),experiment)
result = jobReport.setApplicationStatus(message)
if not result['OK']:
    try:
        with open('job.err', 'a+') as errFile:
            print >> errFile, 'setJobStatus error: %s' % result
    except IOError as e:
        print 'IOError: ',str(e)
