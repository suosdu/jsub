#coding:utf-8
'''
Created on 2015-06-15 19:10:54

@author: suo
'''
import os,shutil
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
    
from optionsParser.OptionsParser import OptionsParser

class CepcRecParser(OptionsParser):
    
    def __init__(self, opts):
        super(CepcRecParser, self).__init__(opts)
        for each in self.opts:
            if os.path.isfile(each) and os.path.basename(each)=='reco.xml':
                self.reco_xml = each
            elif os.path.isfile(each) and os.path.basename(each)=='PandoraLikelihoodData9EBin.xml':
                self.likelihood_data = each
            elif os.path.isfile(each) and os.path.basename(each)=='PandoraSettingsDefault.xml':
                self.settings_default = each
            else:
                print 'Invalid options file: ', each
    
    def __generatePandoras(self,masterdir):
        #----------------------PandoraLikehoodData 不用改,直接拷贝到master下
        shutil.copy(self.likelihood_data, masterdir)
        #----------------------PandoraSettingsDefault 改, 写到master下
        pandoraSD = ET.parse(self.settings_default)
        for element in pandoraSD.findall('algorithm/HistogramFile'):
            element.text = 'PandoraLikelihoodData9EBin.xml'
        pandoraSD.write(os.path.join(masterdir, 'PandoraSettingsDefault.xml'))
        
    def __prepareRecoXml(self):
        recoXML = ET.parse(self.reco_xml)
        for element in recoXML.findall('processor/parameter[@name="PandoraSettingsXmlFile"]'):
            element.text = 'PandoraSettingsDefault.xml'
        return recoXML
    
    def __generateRecoXml(self,subdir,template,inputFilename):#待改，sim可能不做，输入文件名无法这样写
        for element in template.findall('global/parameter[@name="LCIOInputFiles"]'):
            element.text = inputFilename + '_sim.slcio'
        for element in template.findall('processor[@name="MyLCIOOutputProcessor"]/parameter[@name="LCIOOutputFile"]'):
            element.text = inputFilename + '_rec.slcio'
        template.write(os.path.join(subdir, 'reco.xml'))  
         
    def parse(self):
        print 'Enter CepcRecParser.parse()'
        self.recoTemplate = self.__prepareRecoXml()
    
    def generateOpts(self, **kwargs):
        if 'masterDir' not in kwargs:
            print 'masterDir not specified'
        elif 'subDir' not in kwargs:
            print 'subDir not specified'
        elif 'inputFileName' not in kwargs:
            print 'inputFileName not specified'
        else:
            self.__generatePandoras(kwargs['masterDir'])#待改，只需执行一次
            self.__generateRecoXml(kwargs['subDir'], self.recoTemplate, kwargs['inputFileName'])