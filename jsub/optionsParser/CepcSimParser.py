#coding:utf-8
'''
Created on 2015-06-11 22:18:38

@author: suo
'''
import os
from optionsParser.OptionsParser import OptionsParser
from optionsParser.CepcRecParser import CepcRecParser
from splitters.SplitterByFile import SplitterByFile

class CepcSimParser(OptionsParser):
    
    def __init__(self,opts):
        super(CepcSimParser, self).__init__(opts)
        for each in self.opts:
            if os.path.isfile(each) and os.path.basename(each)=='simu.macro':
                self.simu_macro = each
            elif os.path.isfile(each) and os.path.basename(each)=='event.macro':
                self.evemt_macro = each
            else:
                print 'Invalid options file: ',each
                
    def __prepareEventMacro(self,filename):
        template = []
        try:
            with open(filename) as f:
                for eachLine in f:
                    trimedLine = eachLine.lstrip()
                    if trimedLine == '' or trimedLine.startswith('#'):
                        continue
                    else:
                        template.append(trimedLine)
        except IOError as e:
            print 'IOError: ', str(e)
        return template
    
    def __generateEventMacro(self,subdir,template,eventNum,inputFilename):
        try:
            with open(os.path.join(subdir,'event.macro'),'w') as f:
                for line in template:
                    if line.startswith('/generator/generator'):
                        f.write('/generator/generator '+inputFilename+'\n')
                    elif line.startswith('/run/beamOn'):
                        f.write('/run/beamOn '+ repr(eventNum)+'\n')
                    else:
                        f.write(line)
        except IOError as e:
            print 'IOError: ', str(e)
            
    def __prepareSimuMacro(self,filename):
        template = []
        try:
            with open(filename) as f:
                for eachLine in f:
                    trimedLine = eachLine.lstrip()
                    if (trimedLine == '' or trimedLine.startswith('#')):
                        continue
                    elif trimedLine.startswith('/Mokka/init/dbHost'):
                        template.append('/Mokka/init/dbHost 202.114.78.211\n')
                    elif trimedLine.startswith('/Mokka/init/initialMacroFile'):
                        template.append('/Mokka/init/initialMacroFile event.macro\n')
                    else:
                        template.append(trimedLine)
        except IOError as e:
            print 'IOError :',str(e)
        return template
    
    def __generateSimuMacro(self,subdir, template, inputFilenamePre):
        try:
            with open(os.path.join(subdir, 'simu.macro'), 'w') as f:
                for line in template:
                    if line.startswith('/Mokka/init/lcioFilename'):
                        f.write('/Mokka/init/lcioFilename ' + inputFilenamePre + '_sim.slcio\n')
                    else:
                        f.write(line)
        except IOError as e:
            print 'IOError: ',str(e)
            
    def parse(self):
        print 'Enter CepcSimParser.parse()'
        self.eventTemp = self.__prepareEventMacro(self.evemt_macro)
        self.simuTemp  = self.__prepareSimuMacro(self.simu_macro)
    
    def generateOpts(self, **kwargs):
        if 'subDir' not in kwargs:
            print 'subDir not specified'
        elif 'eventNum' not in kwargs:
            print 'eventNum not specified'
        elif 'inputFilename' not in kwargs:
            print 'inputFilename not specified'
        else:
            self.__generateEventMacro(kwargs['subDir'], self.eventTemp, kwargs['eventNum'], kwargs['inputFilename'])
            self.__generateSimuMacro(kwargs['subDir'], self.simuTemp, os.path.splitext(kwargs['inputFilename'])[0])
        
if __name__ == '__main__':
    parser = CepcSimParser(['/home/suo/template/simu.macro','/home/suo/template/event.macro'])
    parser2= CepcRecParser(['/home/suo/template/reco.xml','/home/suo/template/PandoraLikelihoodData9EBin.xml','/home/suo/template/PandoraSettingsDefault.xml'])

    parser.parse()#解析options文件, 结果存到parser的实例属性中
    parser2.parse()

    for filepath, filesize, filename in SplitterByFile().split():#对拆分得到的每项, 生成
        jobPara = {'masterdir':'','subdir':'','eventNum':10,'inputFilename':filename}
        parser.generateOpts(**jobPara)
        parser2.generateOpts(**jobPara)