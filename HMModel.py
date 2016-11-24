'''
author : Praveen Kumar Bodigutla
'''

from ModelBase import ModelBase
from utils import utils
import re

class trellisState():
    def __init__(self,tag,word,previousTags,previousState,previousStates,delta):
        self.tag = tag
        self.word = word
        self.previousTags = previousTags
        self.delta = delta  
        self.previousState = previousState 
        self.previousStates = previousStates
         
    def __str__(self): 
        return "["+self.tag+","+self.word+","+str(self.previousTags)+","+str(self.delta)+"]"
    
    def __repr__(self):
        return self.__str__()  

class Decoder():
    @staticmethod
    def decode(trellis):                
        states = []
        maxdelta = 0.0
        maxdeltaState = None
        for s in trellis[len(trellis)-1]:
            if s.delta >= maxdelta:
                maxdeltaState = s
                maxdelta = s.delta
                
        currentState = maxdeltaState
        states.append(currentState)
        
        while currentState.previousState != None:                
            currentState = currentState.previousState
            states.append(currentState)
                    
        states.reverse()
        return states[1:]

class HMModel(ModelBase):    
    def __init__(self,trainSentences,baseLabels, vocab, HMMOrder = 1,  smoothEmissionCounts = True):
        self._trainingSentences = trainSentences
        self._order = HMMOrder
        self._baseLabels = baseLabels
        self._smoothing = smoothEmissionCounts
        self._vocab = vocab
    
        (self._transitionProbs, self._emissionProbs) = self._getInitialProbabilties(HMMOrder)
        self._trainingLabels = set(map(lambda (x,y):x,self._emissionProbs.keys()))        
    
    def train(self):
        return self._getInitialProbabilties(HMMOrder)
    
    def getLabels(self):
        return self._trainingLabels
     
    def gettrainProbabilities(self):
        return (self._transitionProbs, self._emissionProbs)
    
    def _getInitialProbabilties(self,HMMOrder=1):
        transitionCount = {}
        emissionCount = {}
        transitionProbabilities = {}
        emissionProbabilities = {}        
        totalTransitionCount = 0
        totalTransitionCountByTag = {}
        totalEmissionCount = 0
        totalEmissionCountByTag = {}
        
        for sentence in self._trainingSentences:
            words = sentence.split()
            for x in range(HMMOrder,len(words)):
                previousTags = [] 
                for i in range(x-HMMOrder,x,1):
                    ptoken = words[i]               
                    (pword,plabel) = ptoken.split("_")
                    
                    previousTags.append(plabel)
                            
                    #EmissionCounts and probabilities for the fist 1...HMMOrder-1 (label,word) pairs                
                    if x == HMMOrder:
                        plabel_pword = (plabel,pword)
                        emissionCount = utils.addKeyValueCount(emissionCount,plabel_pword,1)
                        totalEmissionCountByTag = utils.addKeyValueCount(totalEmissionCountByTag,plabel,1)
                        #totalEmissionCount += 1
                        
                previousLabels = tuple(previousTags)
                ntoken = words[x]
                (nword,nlabel) = ntoken.split("_")
                nlabel_nword = (nlabel, nword)
                emissionCount = utils.addKeyValueCount(emissionCount,nlabel_nword,1)
                totalEmissionCountByTag = utils.addKeyValueCount(totalEmissionCountByTag,nlabel,1)
                                            
                plabel_nlabel = (previousLabels,nlabel)
                transitionCount = utils.addKeyValueCount(transitionCount,plabel_nlabel,1)
                transitionCountByTag= utils.addKeyValueCount(totalTransitionCountByTag,previousLabels,1)
                

        #Smoothing Emission Counts        
        if self._smoothing == True:
            numNAWords = 0.0
            for label_word in emissionCount.keys():
                (label,word) = (label_word[0],label_word[1])
                if label == "<NA>":
                    emissionCount[(label,word)] += 1.0
                    numNAWords += 1.0                          
            emissionCount[("<NA>","<UNK>")] = 1.0
            totalEmissionCountByTag["<NA>"] += numNAWords                        
                
        transitionProbabilities = dict(map(lambda (x,y) : (x,(y*1.0)/totalTransitionCountByTag[x[0]]) , transitionCount.items()))
        emissionProbabilities = dict(map(lambda (x,y) : (x,(y*1.0)/totalEmissionCountByTag[x[0]]) , emissionCount.items()))
        
        return(transitionProbabilities, emissionProbabilities)
    
    def validate(self,sentences):
        pass
    
    def test(self,sentences,logFilename,printresults = True):
        results = []
        sentenceNumber = 1.0
        stateStrings = []
        ignoreVocabforNA = False
        f = open(logFilename,'w')
        for sentence in sentences:
            f.write("{}: {} \n".format(sentenceNumber,sentence))
            trellis = self._buildTrellis(sentence, ignoreVocabforNA)
            if trellis != None:
                states = Decoder.decode(trellis)  
                result = (sentence,states)
                #print result
                statestring = ""
                for state in states:
                    statestring += " "+state.tag
                                  
                statestring = statestring.strip()      
                #print statestring
                if printresults == True:
                    f.write(statestring)
                    f.write("\n")
                    
                results.append(result)
            else:
                statestring = "Decoding Failed \n"
                if printresults == True:
                    f.write(statestring)
                #print statestring
            
            stateStrings.append(statestring)    
            sentenceNumber += 1
        
        if printresults == True:    
            (confusionMatrix,Accuracies,Precisions, Recalls, totalAcc) = utils.resultMetrics(results,list(self._baseLabels),self._order)
            strlabel = ""
        
            for label in self._baseLabels:
                label = re.sub("<","",label)
                label = re.sub(">","",label)
                strlabel += " "+label
        
            strlabel = strlabel.strip()
            if printresults == True:
                f.write(strlabel)
                f.write("\n")        
                f.write("Confusion Matrix \n")
                for item in confusionMatrix:
                    outline = "     ".join([str(x) for x in item])
                    outline += "\n"
                    f.write(outline)
                    f.write("\n")
                
                f.write("Accuracy for each bases label\n")            
                for key in Accuracies.keys():
                    outline = key+" : "+str(Accuracies[key]) +"\n"
                    f.write(outline)
                    
                f.write("Precision for each bases label\n")
                for key in Precisions.keys():
                    outline = key + " : "+str(Precisions[key]) +"\n"
                    f.write(outline)
                
                f.write("Recall for each bases label\n")
                for key in Recalls.keys():
                    outline = key + " : "+str(Recalls[key]) +"\n"
                    f.write(outline)
                                 
                f.write("Total Accuracy:{}".format(totalAcc))
                f.close()             
                        
        return stateStrings

    def _buildTrellis(self,sentence,ignoreVocabForNA = False):
        
        words = sentence.split()        
        timeStepIndex = 0
        timeSteps = []
        
        for x in range(self._order,len(words),1):    
            states = []
            #print words[x]
            cword = words[x]
            if len(words[x].split("_")) == 2:
                (cword,clabel) = words[x].split("_")
            
            
            #first non termnial word in the sentence            
            if x == self._order:
                prevTags = []
                startState = None
                
                for i in range(self._order):
                    prevTags.append("<~START~>")
                    
                startState = trellisState("<~START~>","~start~",[],None,None,1.0)
                
                #Check for label not existing
                for label in self._trainingLabels:
                    ptags = tuple(prevTags)
                    plabel_nlabel = (ptags,label)
                    label_cword = (label,cword)
                    delta = 0.0
                    
                    if (self._emissionProbs.has_key(label_cword) == False):
                        if cword not in self._vocab or ignoreVocabForNA == True:                            
                            label_cword = ("<NA>","<UNK>")
                        
                    if ( self._transitionProbs.has_key(plabel_nlabel) == False 
                        or self._emissionProbs.has_key(label_cword) == False):
                        delta = 0.0                        
                    else:
                        delta = self._transitionProbs[plabel_nlabel]*self._emissionProbs[label_cword]*1.0
                    if delta != 0.0:                           
                        st = trellisState(label, cword,prevTags,startState,[startState],delta)
                        states.append(st)
                
            else:        
                for label in self._trainingLabels:
                    deltas = {}
                    prevStates = {}     
                    
                    for s in timeSteps[timeStepIndex-1]:                    
                        prevTags = []
                        prevTags = s.previousTags[1:]
                        prevTags.append(s.tag)
                        prevLabels = tuple(prevTags)
                        plabel_nlabel = (prevLabels,label)
                        label_cword = (label, cword)
                        prevStates[plabel_nlabel] = s

                        #Taking care of unknown word
                        if (self._emissionProbs.has_key(label_cword) == False):
                            if cword not in self._vocab or ignoreVocabForNA == True:
                                label_cword = ("<NA>","<UNK>")
                            
                        if ( self._transitionProbs.has_key(plabel_nlabel) == False 
                                or self._emissionProbs.has_key(label_cword) == False):
                            deltas[plabel_nlabel] = 0.0
                            prevStates[plabel_nlabel] = s
                        else:
                            delta = self._transitionProbs[plabel_nlabel]*self._emissionProbs[label_cword]*s.delta
                            deltas[plabel_nlabel] = delta
                            prevStates[plabel_nlabel] = s
                
                    
                    maxdeltavalue = max(deltas.values()) 
                    maxdeltaKeys = [k for k in deltas.keys() if deltas[k] == maxdeltavalue]
                    
                    if maxdeltavalue == 0:
                        continue

                    #if len(maxdeltaKeys) > 1:
#                     print "more than one possible previous state for label: {}, word:{}".format(label,cword)
#                     bestPrevStates = []
#                     bestPrevTags = []                         
#                     for key in maxdeltaKeys:
#                         bestPrevTag = list(key[0])
#                         bestPrevState = prevStates[key]
#                         if bestPrevTag not in bestPrevTags:
#                             bestPrevTags.append(bestPrevTag)
#                             bestPrevStates.append(bestPrevState)                     
#                         #redundant to check for maxValue
                    
                    #arbitrary pick one delta key
                    bestPreviousTagDelta = maxdeltaKeys[0]
                    bestPreviousTags = list(bestPreviousTagDelta[0])
                    bestPreviousState = prevStates[bestPreviousTagDelta]
                    st = trellisState(label, cword,bestPreviousTags,bestPreviousState, None,maxdeltavalue)                      
                    states.append(st)
            
            if len(states) == 0:
                return None
            
            #print "Printing states for index:{}".format(timeStepIndex)
            #utils.print_ds(states)            
            timeSteps.append(states)
            
            timeStepIndex += 1
                        
        return timeSteps        
                        
            



    

    
    
    
    
