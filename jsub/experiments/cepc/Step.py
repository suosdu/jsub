'''
Created on 2015-06-01 12:54:09

@author: suo
'''
from experiments.Step import Step
from optionsParser.CepcSimParser import CepcSimParser
from optionsParser.CepcRecParser import CepcRecParser

class Sim(Step):
    def __init__(self,stepDict = None, name = None):
        super(Sim, self).__init__(stepDict)
        self.number = '1'
        self.optionsParser = CepcSimParser(self.jobOption)
        self.description = 'This is Cepc Sim: '+name
        print self.description

class Rec(Step):
    def __init__(self,stepDict = None, name = None):
        super(Rec, self).__init__(stepDict)
        self.number = '2'
        self.optionsParser = CepcRecParser(self.jobOption)
        self.description = 'This is Cepc Rec: '+name
        print self.description

if __name__ == '__main__':
    s = Sim()