'''
author : Praveen Kumar Bodigutla
'''
import re
import math
from sklearn.metrics import confusion_matrix
import numpy as np
import matplotlib.pyplot as plt
import itertools
import logging

class utils:
    @staticmethod
    def print_ds(a):
        if type(a) is type(None):
            print "NULL"
        elif type(a) is str:
            print "\"{}\"".format(a)
        elif type(a) is list:
            for x in a:
                print x
        elif type(a) is dict:
            for (key,value) in a.iteritems():
                print "{} : {}".format(key,value)
        elif type(a) is tuple:
            for t in a:
                print "{}".format(t)
        else:
            raise KeyError ("Unidentified Type:{}".format(a))      
        
        return
    
    @staticmethod    
    def process(text):
        text = re.sub("[!$+]","", text)
        text = re.sub(":_","_",text)
        text = re.sub("[-();]"," ",text)
        text = re.sub("\.","", text)
        text = re.sub("([:/%])",lambda x:" "+x.group(1)+" ", text)
        text = re.sub("(\d)th", lambda x:x.group(1),text)
        text = re.sub("(\d+)([a-zA-Z]+)", lambda x:x.group(1)+" "+x.group(2),text)
        text = re.sub("([a-zA-Z]+)(\d+)", lambda x:x.group(1)+" "+x.group(2),text)
        text = re.sub("'s_","_",text)
        text = re.sub("(\w+)s'_",lambda x:str(x.group(1))+"_" , text)
        #text = re.sub("(\w+)'(\w+)?_(\w+)",lambda x:str(x.group(1)+"_"+str(x.group(3))),text)
        text = re.sub("'","",text)        
        text = re.sub("\s+"," ",text)        
        return text   
    
    @staticmethod
    def getLogger():
        logger = logging.getLogger('timeParser')
        logger.setLevel(logging.DEBUG)        
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        return logger
        
        
    @staticmethod
    def addKeyValue(d, key, value):
        
        if (key is None) or (value is None) :
            return d        
        if (d is None):
            d = {}
            d[key] = [value]
            return d
        
        if key in d.keys():
            if value not in d[key]:
                d[key].append(value)
        else:
            d[key] = [value]
        return d

    @staticmethod
    def addKeyValueCount(d,key,value):
        if key is None or value is None:
            return d
        
        if d is None:
            d = {}
            d[key] = value
            return  d
        
        if key in d.keys():
            d[key] += value
        else:
            d[key] = value 
        
        return d

    @staticmethod            
    def getDictValue(d,key,defaultValue):
        if d == None or d.has_key(key) == False:
            return defaultValue
        else:
            return d[key]
        
    @staticmethod
    def splitSentences(data,tratio,vratio,shuffle=False,returnVocab=True):
        
                
        if data == None:
            raise ValueError
        
        
        indicies = np.arange(len(data))
        
        if shuffle == True:
            np.random.shuffle(indicies)
            shuffleddata = [data[i] for i in indicies]
            data = shuffleddata
        
        print indicies
        if tratio <=0  or data is None or (tratio+vratio) > 1.0:
            raise ValueError
        
        tlen = int(math.floor(tratio*len(data)))
        vlen = int(math.floor(vratio*len(data)))
        
        print "numtrain:",tlen
        print "numvalidate:",vlen
        print "numtest:",len(data)-(tlen+vlen)
        
        trainingSet = data[0:tlen]
        trainIndicies = indicies[0:tlen]
        
        vocab = []        
        if returnVocab == True:    
            for s in trainingSet:
                for w_l in s.split():
                    (w,l) = w_l.split("_")
                    if w not in vocab:
                        vocab.append(w)
            
        validateSet = data[tlen:tlen+vlen]
        validateIndicies = indicies[tlen:tlen+vlen]
        
        testSet = data[tlen+vlen:len(data)]
        testIndicies = indicies[tlen+vlen:len(data)]
        
        if returnVocab == True:
            return(trainingSet,validateSet,testSet,trainIndicies,validateIndicies,testIndicies,vocab)
        else:
            return(trainingSet,validateSet,testSet,trainIndicies,validateIndicies,testIndicies)
    
                
    @staticmethod
    def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    
        plt.imshow(cm, interpolation='nearest', cmap=cmap)
        plt.title(title)
        plt.colorbar()
        tick_marks = np.arange(len(classes))
        plt.xticks(tick_marks, classes, rotation=45)
        plt.yticks(tick_marks, classes)

        if normalize:
            cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
            print("Normalized confusion matrix")
        else:
            print('Confusion matrix, without normalization')

        print(cm)

        thresh = cm.max() / 2.
        for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
            plt.text(j, i, cm[i, j],
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

        plt.tight_layout()
        plt.ylabel('True label')
        plt.xlabel('Predicted label')
    
            
    @staticmethod
    def resultMetrics(results,trainingLabels,wordsToSkip=2):
        
        if wordsToSkip <0 :
            raise ValueError
        
        truelabelTotalCount = {}
        predictedlabelTotalCount = {}
        truelabelPredictedCount = {}
        
        trueLabels = []
        predLabels = []
        
        for result in results:
            trueSentence = result[0]
            predictedLabels = result[1]            
            words = trueSentence.split()
            predLabelIndex = 0
            
            for i in range(wordsToSkip,len(words)-wordsToSkip,1):
                word_label = words[i]
                (word,label) = word_label.split("_")
                trueLabels.append(label)
                truelabelTotalCount = utils.addKeyValueCount(truelabelTotalCount, label, 1.0)
                
                predictedLabel = predictedLabels[predLabelIndex].tag
                predictedlabelTotalCount = utils.addKeyValueCount(predictedlabelTotalCount,predictedLabel, 1.0)                                                
                predLabels.append(predictedLabel)
                truelabelPredictedCount = utils.addKeyValueCount(truelabelPredictedCount, (label,predictedLabel), 1.0)
                
                predLabelIndex += 1
                
        datalabels  = list(set(trueLabels))
        
        #print trainingLabels
        cmatrix = confusion_matrix(trueLabels, predLabels, labels=trainingLabels)
                
        Accuracies = {}
        Precisions = {}
        Recalls = {}

        #for label in truelabelTotalCount.keys():
        totalCorrect = 0.0
        totalInstances = 0.0

        for label in trainingLabels:
            truePredictionKey = (label,label)
            tp = utils.getDictValue(truelabelPredictedCount, truePredictionKey,0.0)
            labelTrueCount = utils.getDictValue(truelabelTotalCount,label,0.0)
            labelPredictedCount = utils.getDictValue(predictedlabelTotalCount,label,0.0)
            
            if label in trueLabels:
                if tp != 0:
                    Accuracies[label] = tp/(labelTrueCount + labelPredictedCount - tp)
                    Precisions[label]  = tp/labelPredictedCount
                    Recalls[label] = tp/labelTrueCount
                else:
                    Accuracies[label] = 0.0
                    Precisions[label] = 0.0
                    Recalls[label] = 0.0
                
            totalCorrect += tp
            totalInstances += labelTrueCount            
            
        totalAccuracy = totalCorrect/totalInstances        
        
        return (cmatrix, Accuracies,Precisions,Recalls, totalAccuracy)
    
    @staticmethod
    def comparePlot(filename, arrayTuples,index1,index2,title):
        ft = open(filename,'wb')
        sortedTuples = sorted(arrayTuples,key = lambda x:x[index1])
        numElements = len(arrayTuples)
        vector1 = []
        vector2 = []
        
        matchCount = 0.0
        for elements in sortedTuples:
            vector1.append(elements[index1])
            vector2.append(elements[index2])
            if elements[index1] == elements[index2]:
                matchCount += 1.0
            else:
                sentence = elements[0]+"\n"
                ft.write(sentence)
        xaxis = range(numElements)
        ft.close()
        print "Accuracy:{}".format(matchCount/numElements)
        plt.suptitle(title)
        plt.plot(xaxis, vector1,'bs',xaxis,vector2, 'g^')
        #plt.legend(handles=[trueLabels,predLabels])
        tL, = plt.plot(xaxis,vector1, 'bs', label="Actual Time")
        pL, = plt.plot(xaxis,vector2, 'g^', label="Predicted Time")
        plt.legend([tL, pL], ['Actual Time','Predicted Time'],loc=4)
        plt.ylabel('Predicted Time and Actual Time')
        plt.xlabel('Index')
        plt.ylim((min(vector1)-10000,max(vector1)+10000))
        plt.show()
        
            
    @staticmethod
    def writePredictedResultsToFile(results,filename):
        ft = open(filename,'wb')
        #(os,s,t,predictedBeginTime,trueBeginTime,predictedEndTime,trueEndTime)
        #predictedResults.append((os,s,t,predictedBeginTime,trueBeginTime,predictedEndTime,trueEndTime,trueBeginTimeStr,beginTimestring,trueEndTimeStr,endTimestring))
        for result in results:
            printstring = result[0]+","+result[2]+",predictedBegin:"+result[8]+",trueBegin:"+result[7]+",predictedEnd:"+result[10]+",trueEnd:"+result[9]+"\n"
            ft.write(printstring)
        ft.close()
            
    
    
        
    
        
        