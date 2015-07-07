'''
Created on 2015-06-02 17:14:28

@author: suo
'''
from experiments.Step import Step
# 
# def foo():
#     print 'This is foo'
 
class Sim(Step):
    def __init__(self, stepDict = None, name = None):
        super(Sim, self).__init__(stepDict)
        self.number = '1'
        print 'This is Bes Sim: ',name

class Rec(Step):
    def __init__(self, stepDict = None, name = None):
        super(Rec, self).__init__(stepDict)
        print 'This is Bes Rec: ',name
        self.number = '2'

class Ana(Step):
    def __init__(self, stepDict = None, name = None):
        super(Ana, self).__init__(stepDict)
        print 'This is Bes Ana: ',name
        self.number = '3'
        
if __name__ == '__main__':
    s = Sim()
    print s.__dict__
    print s.number