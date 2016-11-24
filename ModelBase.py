'''
author : Praveen Kumar Bodigutla
'''
from abc import ABCMeta, abstractmethod

class ModelBase:
    __metaclass__ = ABCMeta

    @abstractmethod
    def train(self, trainingData):
        pass
    
    @abstractmethod
    def validate(self, validateData):
        pass
    
    @abstractmethod
    def test(self, testData):
        pass    
    
    