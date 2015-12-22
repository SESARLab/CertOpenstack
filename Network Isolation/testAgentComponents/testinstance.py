__author__ = 'Patrizio Tufarolo'
__email__ = 'patrizio.tufarolo@studenti.unimi.it'

class TestInstance(object):
    def __init__(self,operation):
        self.__preConditions = ""
        self.__hiddenCommunications  = ""
        self.__expectedOutput = ""
        self.__postConditions = ""
        self.__input = {}
        self.__operation = operation

    def getOperation(self):
        return self.__operation

    def setPreConditions(self,pc):
        self.__preConditions = pc
        return

    def getPreConditions(self):
        return self.__preConditions

    def setHiddenCommunications(self,hc):
        self.__hiddenCommunications = hc
        return

    def getHiddenCommunications(self):
        return self.__hiddenCommunications

    def appendInput(self,key,value):
        self.__input[key] = value
        return
    def getInputs(self):
        return self.__input

    def setExpectedOutput(self,eo):
        self.__expectedOutput = eo
        return

    def getExpectedOutput(self):
        return self.__expectedOutput

    def setPostConditions(self,pc):
        self.__postConditions = pc
        return

    def getPostConditions(self):
        return self.__postConditions