'''
author : Praveen Kumar Bodigutla
'''
from abc import ABCMeta

from datetime import datetime
from datetime import date
import operator
import csv
import time
import re

from utils import utils
from HMModel import HMModel
from translator import BeginEndTime
from fileinput import filename

class rawtimeDataFromFile():
    def __init__(self, filename):
        self._filename = filename
    def __process(self,text):
        
        text = re.sub(":_","_")
        text = re.sub("[!-]"," ", text)
        #text = re.sub("'s","",text)
        text = re.sub("([:/])",lambda x:" "+x.group(1)+" ", text)
        text = re.sub("(\d)th", lambda x:x.group(1),text)
        text = re.sub("(\d+)([a-zA-Z]+)", lambda x:x.group(1)+" "+x.group(2),text)
        #To take care of words like president's, april's etc...
        text = re.sub("'","",text)        
        return text
    
    def getSentences(self):
        uniqueTimeSentences = {}
        try:
            with open(self._filename,'r') as f:
                lines = f.readlines()
                for line in lines:
                    if "~__t" in line:
                        times = re.findall("~\(([^~]*)\)~__t",line)
                        for time in times:
                            if not uniqueTimeSentences.has_key(time):
                                time = self.__process(time)
                                print time
                                uniqueTimeSentences[time] = 1
        except IOError as e:
            print "Can not open file:{}".format(self._filename)
            print "Error Message:{}".format(e)
        
        return uniqueTimeSentences.keys()

class readUnLabeledData():
    logger = utils.getLogger()
    def __init__(self,filename,numTerminalTags):
        self.__filename = filename
        (self.__processedSentenceTimeTuples,self.__processedSentenceOriginalSentenceMap) = self.__returnProcessedTuples(numTerminalTags)
        #utils.print_ds(self.__processedSentenceTimeTuples)
        
    def __returnProcessedTuples(self,numTerminalTags):
        uniqueTimeSentences = []
        sentenceTimeTuples = {}
        processedOldSentenceMap = {}
        
        try:
            with open(self.__filename,'rb' ) as csvtestfile:
                datareader = csv.DictReader(csvtestfile)
                for row in datareader:
                    #print row
                    originalSentence = utils.process(row['sentence'])
                    processedSentence = self._process(originalSentence)
                    for i in range(numTerminalTags):                        
                        processedSentence = "<~start~>_<~START~> "+processedSentence+" <~end~>_<~END~>"
                    reftime = row['refTime']
                    
                    if processedSentence not in uniqueTimeSentences:
                        uniqueTimeSentences.append(processedSentence)
                        sentenceTimeTuples[processedSentence] = (reftime)
                        processedOldSentenceMap[processedSentence] = originalSentence
                        
        except IOError as e:
            readUnLabeledData.logger.error("Can not open file :{}, {}".format(self.__filename,e))
        
        return (sentenceTimeTuples, processedOldSentenceMap)
    
    def getProcessedSentenceTuples(self):
        return self.__processedSentenceTimeTuples
    
    def getOrignialSentence(self,processedSentence):
        return utils.getDictValue(self.__processedSentenceOriginalSentenceMap, processedSentence,None)
    
    def _process(self,sentence):
        sentence = sentence.strip()
        words = sentence.split()
        processedSentence = []
        for word in words:
            try:
                int(word)
                processedSentence.append("DIGIT")
            except ValueError:
                processedSentence.append(word.lower())
        return  " ".join(processedSentence)
                
    
class readLabeledData():
    
    logger = utils.getLogger()
    def __init__(self,filename):
        self.__filename = filename
    
    def getLabledTuples(self):
        uniqueTimeSentences = []
        sentenceTimeTuples = {}
        
        try:
            with open(self.__filename,'rb') as csvtrainfile:
                datareader = csv.DictReader(csvtrainfile)
                for row in datareader:
                    sentence = row['labeledSentence']
                    sentence = utils.process(row['labeledSentence'])
                    
                    reftime  = row['refTime']
                    begintime = row['beginTime']
                    endtime = row['endTime']
                    
                    if sentence not in uniqueTimeSentences:
                        uniqueTimeSentences.append(sentence)
                        sentenceTimeTuples[sentence] = (reftime,begintime,endtime)
                                            
        except IOError as e:
            readUnLabeledData.logger.error("Can not open file:{}, {}".format(self.__filename,e))

        return sentenceTimeTuples


class labeledSentencesProcessor():
    logger = utils.getLogger()
    def __init__(self,sentences,numTerminalTags=1,numValidTags=2):
        self._baseLabels = [
                            "<ETPYN>", "<ETPDS>","<ETPDN>", "<ETPMS>", "<ETPMN>", "<ETPHS>", "<ETPHN>", "<ETPmN>","<ETPmS>", "<ETPAP>","<ETPZ>",
                            "<BTPYS>", "<BTPYN>", "<BTPDS>","<BTPDN>", "<BTPMS>", "<BTPMN>", "<BTPHS>", "<BTPHN>", "<BTPmN>", "<BTPmS>", "<BTPAP>", 
                            "<BTPZ>", "<TDPS>" , "<TDPN>" , "<TDSS>" , "<TDSN>" , "<TPRD>"
                            ]
                
        (self._labelWords, self._filesentences) = self.__parseLabeledData(sentences, numTerminalTags,numValidTags)
        
    def _isbaseLabel(self,word_label):    
        for label in self._baseLabels:
            #Remove the <> while comparing because training data does not have <>
            label = label[1:len(label)-1]
            if label in word_label:
                return True
        return False
    
    def _returnWordLabel(self,word,addlabel,label):
        monthL = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december'];
        monthS = ['jan', 'feb', 'mar', 'apr', 'may', 'june', 'july', 'aug', 'sept', 'oct', 'nov', 'dec'];
        dayL = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        dayS = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']

        try:
            int(word)
            if addlabel == True:
                if label is None:
                    label = "<DIGIT>"

                return ("DIGIT",label)
            else:
                label = "<NA>"
                return ("DIGIT","<NA>")            
        except ValueError:
            if addlabel == True:
                if label is None:    
                    label = "<"+word.upper()+">"
            else:
                return (word.lower(),"<NA>")
                
            return(word.lower(),label)
    

    def _process(self,word_label,index,numValidTags,words):
        
        addlabel = False
        
        if numValidTags == -1:
            addlabel = True
        
        else:
            for i in range(index-(numValidTags),index+numValidTags+1,1):
                if i>=0 and i<len(words):
                    if self._isbaseLabel(words[i]) ==True:
                        addlabel = True  
                
        if "_" in word_label:
            (word, label) = word_label.split("_")
            
            label = "<"+label+">"
            if word == '' and label == '<>':
                return ("<UDERSCORE>", "<NA>")
            else:
                if word == '' or label == '':
                    raise KeyError  
            return self._returnWordLabel(word, addlabel, label)
        
        else:
            return self._returnWordLabel(word_label, addlabel, None)
         
        
    def __parseLabeledData(self,insentences,numTerminalTags,numValidTags):
        sentences = []
        labelWords = {}
        
        for line in insentences:
            line = line.strip()
            words = line.split()
            tokens = []
            index = 0
            
            for fullword in words:    
                (word,label) = self._process(fullword,index,numValidTags,words)
                labelWords = utils.addKeyValue(labelWords,label,word)  
                                                    
                token = word+"_"+label
                tokens.append(token)
                index = index + 1  
            
            processedline = " ".join(tokens)
            for i in range(numTerminalTags):                        
                processedline = "<~start~>_<~START~> "+processedline+" <~end~>_<~END~>"

            sentences.append(processedline)
                            
        return (labelWords,sentences)


    def gettrainLabels(self):
        return self.getLabelWords().keys()
                
    def getSentences(self):
        return self._filesentences
    
    def getLabelWordsMap(self):
        return self._labelWords
    
    def getBaseLabels(self):
        return self._baseLabels
    
    def getUnProcessedLines(self):
        return self._unprocessedLines
        
def loadTranslateUnlabeledData(testDataFile, outputfile):
    #HMMOrder
    order = 1
      
    #ContextWindow
    windowSize = 2
              
    #InputData Filename
    filename = "data/labeledsentences.csv"
           
    #A map of sentence to timeTuples
    inputData = readLabeledData(filename).getLabledTuples()
   
    #Process the labeled data    
    inputSentences = inputData.keys()
    labeledData = labeledSentencesProcessor(inputSentences, order, windowSize)
    processedSentences = labeledData.getSentences()    
    assert(len(inputData.keys())==len(processedSentences))
      
    labelWords = labeledData.getLabelWordsMap()
       
    #Split the data, number of records in train and validate sets is specified here, the rest is considered testdata
    #Vocabulary is obtained from training data, this is useful when we handle unknown words
    #Train on entire labeled data
    #tri = shuffled indicies training data
    #vai = shuffled indicies validate data
    #tei = shuffled indicies test data
    
    (train,validate,test,tri,vai,tei,vocab) = utils.splitSentences(processedSentences,1.0, 0, shuffle=True, returnVocab=True)
    
    baseLabels = labeledData.getBaseLabels()
    
    model = HMModel(train, baseLabels, vocab, order, True)
      
    #Process test sentences
    testUnlabeledData = readUnLabeledData(testDataFile,order)
    testProcessedSentenceTuples = testUnlabeledData.getProcessedSentenceTuples()
    testSentences = testProcessedSentenceTuples.keys()
    
    testResultStrings = model.test(testSentences,outputfile,False)    
    assert(len(testSentences) == len(testResultStrings))
    
    resultTuples = []
    for x in range(len(testSentences)):
        
        s = testSentences[x]
        refTime = testProcessedSentenceTuples[s]
        
        os = testUnlabeledData.getOrignialSentence(s)
        t = testResultStrings[x]
        if "Decoding Failed" in t:
            labeledSentencesProcessor.logger.debug("Decoding failed for sentence :{}".format(os))
            continue
        
        targetWords  = t.split()
        sourceWords = os.split()
        targetIndex = 0
        baseLabelWordTuples = []

        for word in targetWords:
            if word == "<~START~>":
                targetIndex += 1
                 
        
        for w in sourceWords:          
            targetLabel =  targetWords[targetIndex]            
            if targetLabel in baseLabels:
                label_word = (targetLabel,w.lower())
                baseLabelWordTuples.append(label_word)
            targetIndex += 1
                    
        bet = BeginEndTime(baseLabelWordTuples, refTime)
        beginTime = bet.getBeginTime()
        endTime = bet.getEndTime()
        beginTimestring = str(beginTime['month'])+"/"+str(beginTime['day'])+"/"+str(beginTime['year'])+" "+str(beginTime['hour'])+":"+str(beginTime['minute'])    
        endTimestring = str(endTime['month'])+"/"+str(endTime['day'])+"/"+str(endTime['year'])+" "+str(endTime['hour'])+":"+str(endTime['minute'])
        
        resultTuple = (os, s, t, refTime, beginTimestring, endTimestring)
        resultTuples.append(resultTuple)
    
    return resultTuples
    

def loadTranslateTestLabeledData(outputFile):
    #HMMOrder
    order = 1
          
    #ContextWindow
    windowSize = 2
              
    #InputData Filename
    filename = "data/labeledSentences.csv"
           
    #A map of sentence to timeTuples
    inputData = readLabeledData(filename).getLabledTuples()
   
    #Process the labeled data    
    inputSentences = inputData.keys()
    labeledData = labeledSentencesProcessor(inputSentences, order, windowSize)
    processedSentences = labeledData.getSentences()    
    assert(len(inputData.keys())==len(processedSentences))
      
    labelWords = labeledData.getLabelWordsMap()
       
    #Split the data, number of records in train and validate sets is specified here, the rest is considered testdata
    #Vocabulary is obtained from training data, this is useful when we handle unknown words
    #tri = shuffled indicies training data
    #vai = shuffled indicies validate data
    #tei = shuffled indicies test data
    (train,validate,test,tri,vai,tei,vocab) = utils.splitSentences(processedSentences,0.8, 0, shuffle=True, returnVocab=True)
       
    #Specifying the model
    baseLabels = labeledData.getBaseLabels()
    model = HMModel(train, baseLabels, vocab, order, True)

    #Labeled Results
    resultStrings = model.test(test,outputFile)    
    assert(len(test) == len(resultStrings))
    assert(len(test) == len(tei))
         
    predictedResults = []     
         
    for x in xrange(len(test)):
        
        #processed source sentence
        s = test[x].strip()
        #Labeled result
        t = resultStrings[x].strip()
        os = inputSentences[tei[x]]
        
        if "Decoding Failed" in t:
            labeledSentencesProcessor.logger.debug("Decoding failed for sentence {}".format(os))
            continue
        #ActualInputSentence
        #os = inputSentences[tei[x]]
        timeTuple = inputData[os]
              
        sourceWords = os.split()
        targetWords = t.split()
             
        targetIndex = 0
        baseLabelWordTuples = []
              
        for word in targetWords:
            if word == "<~START~>":
                targetIndex += 1
                  
        for sourceWord in sourceWords:
            w = sourceWord
            if "_" in sourceWord:
                (w,l) = sourceWord.split("_")            
                 
            targetLabel =  targetWords[targetIndex]            
            if targetLabel in baseLabels:
                label_word = (targetLabel,w.lower())
                baseLabelWordTuples.append(label_word)
            targetIndex += 1 
                     
        bet = BeginEndTime(baseLabelWordTuples,timeTuple[0])
        beginTime = bet.getBeginTime()
        endTime = bet.getEndTime()
    
        trueBeginTimeStr = timeTuple[1]
        trueBeginTimedt = time.strptime(trueBeginTimeStr, "%m/%d/%y %H:%M")
        trueEndTimeStr = timeTuple[2]
        trueEndTimedt = time.strptime(trueEndTimeStr, "%m/%d/%y %H:%M")
            
        predictedBeginTime = int(datetime(beginTime['year'],beginTime['month'],beginTime['day'],beginTime['hour'],beginTime['minute']).strftime('%s'))
        predictedEndTime = int(datetime(endTime['year'],endTime['month'],endTime['day'],endTime['hour'],endTime['minute']).strftime('%s'))
        trueBeginTime = int(datetime(trueBeginTimedt.tm_year,trueBeginTimedt.tm_mon,trueBeginTimedt.tm_mday,trueBeginTimedt.tm_hour,trueBeginTimedt.tm_min).strftime('%s'))
        trueEndTime = int(datetime(trueEndTimedt.tm_year,trueEndTimedt.tm_mon,trueEndTimedt.tm_mday,trueEndTimedt.tm_hour,trueEndTimedt.tm_min).strftime('%s'))
        beginTimestring = str(beginTime['month'])+"/"+str(beginTime['day'])+"/"+str(beginTime['year'])+" "+str(beginTime['hour'])+":"+str(beginTime['minute'])+"\n"    
        endTimestring = str(endTime['month'])+"/"+str(endTime['day'])+"/"+str(endTime['year'])+" "+str(endTime['hour'])+":"+str(endTime['minute'])+"\n"

        predictedResults.append((os,s,t,predictedBeginTime,trueBeginTime,predictedEndTime,trueEndTime,trueBeginTimeStr,beginTimestring,trueEndTimeStr,endTimestring))            
    return predictedResults
    



 