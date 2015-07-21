#coding:utf-8
'''
Created on 2015-05-27 12:03:18

@author: suo
'''
import sys,yaml,copy,pprint
from DIRAC.Core.Base import Script
Script.parseCommandLine( ignoreErrors = False )

sys.path.append('/home/cc/suob/jsub/jsub')
#sys.path.append('/home/cc/suob/jsub/e')
from __builtin__ import __import__
from utility.DataRegister import registerInputData
'''1.读取yaml文件'''
print '1.'
try:
    with open('CepcJob.yaml') as f:
        x = yaml.load(f)
except Exception as e:
    print 'Exception: ',str(e)
# '''*实例化steps'''
# '''第一种实例化类的方法'''
# classStr = 'module.%s(name = "mokka")' % ('Sim')
# classInstance1 = eval(classStr)
# '''第二种实例化类的方法'''
# classInstance2 = getattr(module, 'Rec')(name = 'marlin')
# functionInstance = getattr(module, 'foo')()

# jobSteps = sorted(copy.deepcopy(x['Experiment']['JobSteps']),
#                   key = lambda step:step['Type'],reverse = True)
jobSteps = x['Experiment']['JobSteps']
'''2.检查,steps不能有重复的'''
print '2.'
stepTypes = []
for step in jobSteps:
    print step['ReturnData']
    if step['Type'] not in stepTypes:
        stepTypes.append(step['Type'])
    else:
        print 'duplicated step: ',step['Type']
        stepTypes = None
        break
print stepTypes

'''3.steps序列要求(做哪几步),有跳步的报错'''
#这种方式需要记录的情况太多，不太灵活，考虑其他方案。。。
# print '3.'
# stepsTag = 0
# for each in stepTypes:
#     if each == 'Sim':
#         stepsTag+=1
#     elif each == 'Rec':
#         stepsTag+=2
#     elif each == 'Ana':
#         stepsTag+=4
#     else:
#         print 'step Type Error'
#         stepsTag = 0
#         break
# print stepsTag
# 
# if stepsTag == 1:
#     print 'Steps: Sim'
# elif stepsTag == 2:
#     print 'Steps: Rec'
# elif stepsTag == 4:
#     print 'Steps: Ana'
# elif stepsTag == 3:
#     print 'Steps: Sim+Rec'
# elif stepsTag == 6:
#     print 'Steps: Rec+Ana'
# elif stepsTag == 7:
#     print 'Steps: Sim+Rec+Ana'
# else:
#     print 'Steps Specification Error'
    
'''4.创建steps列表'''
print '4.'
try:
    exprimentPlugin = 'experiments.%s.Step' % x['Experiment']['Name']
    module = __import__(exprimentPlugin,globals(),locals(),[''])
except Exception as e:
    print 'Exception: ',str(e)
print dir(module)

stepList = []
stepNumList = []
for step in jobSteps:
    stepList.append(getattr(module, step['Type'])(stepDict = step,name = step['Executable']))
print stepList

'''按照Sim, Rec, (Cali,) Ana的顺序排列'''
sorted_jobSteps = sorted(stepList,key = lambda step:step.number)

   
'''''''''''''''获取splitter'''''''''''
splitterName = 'Splitter%s' % x['Splitter']['Type']
try:
    splitterPath = 'splitters.'+splitterName
    module = __import__(splitterPath, globals(), locals(),[''])
except Exception as e:
    print 'Exception: ',str(e)
    
splitter = getattr(module, splitterName)(splitterDict = x['Splitter'])

'''''''''''''''获取workflow'''''''''''
workflowName = '%sWorkflow' % (x['Experiment']['Name'][0].upper()+x['Experiment']['Name'][1:])
try:
    workflowPath = 'workflow.'+workflowName
    module = __import__(workflowPath, globals(), locals(),[''])
except Exception as e:
    print 'Exception: ',str(e)
workflow = getattr(module, workflowName)()

'''''''''''''''获取backend'''''''''''
backendName = x['Backend']['Name']
try:
    backendPath = 'backend.'+backendName
    module = __import__(backendPath, globals(), locals(), [''])
except Exception as e:
    print 'Exception: ',str(e)
backend = getattr(module, backendName)(backendDict = x['Backend'])
print backend.getDFCprefix()
'''''''''''''''获取jobFactory'''''''''''
jobfactoryName = '%sJobFactory' % (x['Experiment']['Name'][0].upper()+x['Experiment']['Name'][1:])
try:
    jobfactoryPath = 'jobfactory.'+jobfactoryName
    module = __import__(jobfactoryPath,globals(),locals(),[''])
except Exception as e:
    print 'Exception: ',str(e)
jobFactory = getattr(module, jobfactoryName)()
 
for step in sorted_jobSteps:
    print step.__dict__
    step.optionsParser.parse()#每一个step，解析options文件
    stepNumList.append(step.number)

subjobs = jobFactory.createSubJobs(x['Experiment']['Name'],splitter,backend,stepNumList)
workflow.setJobSteps(sorted_jobSteps)
workflow.setStepNumList(stepNumList)


for subjob in subjobs:
    try:
        with open(os.path.join(subjob['subDir'],'jobParam')) as f:
            pprint.pprint(subjob,f)
    except IOError as e:
        print 'IOError',str(e)
    registerInputData(subjob['inputFilePath'],subjob['inputFileSize'])
    for step in sorted_jobSteps:
        step.optionsParser.generateOpts(**subjob)#每一个step,生成opts文件
    workflow.updateForSubjob(jobParam = subjob)
    workflow.generateScript()
    result = backend.submit(subjob)

    print subjob['jobName']
'''
    if result['OK']:
        print 'Job %s submitted successfully. ID = %d' %(subjob['jobName'],result['Value'])
    else:
        print 'Job %s submitted failed' %subjob['jobName']
'''
