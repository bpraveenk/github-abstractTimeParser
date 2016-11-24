import dataParser
from utils import utils
import logging
import time

def main():
     
    start_time = time.time()
    #This file contains the processed sentence and the predicted labels
    #It also contains recall, precision and accuracy values for individual label
    #Shows confusion matrix on labels
    outputfile = "results/output_label_predictionResults.txt"
     
    #Contains lines for which the begin time is different from predicted start time
    outputMismatchBeginFile = "results/output_beginTimeMismatch.txt"
     
    #Contains lines for which the end time is different from predicted end time
    outputMismatchEndFile = "results/output_endTimeMismatch.txt"
     
    # Results are returned as tuples of 
    #(original sentence,processed sentence,predicted Sentence
    #,predictedBeginTime (epoch),trueBeginTime (epoch),predictedEndTime (epoch),trueEndTime (epoch),
    #trueBeginTimeStr (mm/dd/yy %H:%m:%s),predictedBeginTimestring (mm/dd/yyyy %H:%m:%s),
    #trueEndTimeStr (mm/dd/yy %H:%m:%s), predictedEndTimestring (mm/dd/yyyy %H:%m:%s)))     
    predictedResults = dataParser.loadTranslateTestLabeledData(outputfile)
    
    # Print all predictedResults to file for debugging
    #resultsFileName = "results/output_predictedTimes.txt"
    #utils.writePredictedResultsToFile(predictedResults,resultsFileName)
     
    #True<begin|end>time index, predicted (begin|end) time index
    utils.comparePlot(outputMismatchBeginFile,predictedResults,4,3,"Begin Time Comparison")
    utils.comparePlot(outputMismatchEndFile,predictedResults,6,5, "End Time Comparison")
    
    elapsed_time = time.time() - start_time
    print (elapsed_time)
    #For unlabeled sentences
      # processed sentences for generic test input  
#     outputTestFile = "results/output_test_processedSentences.txt"
#         
#       # Input file where general unlabled sentences are stored
#       # input format "refdate, sentence" - one per line in the file  
#     testInputFile = "data/unlabeledSentences.csv"
# 
#       
#       # Results are returned as list of tuples where each tuple is 
#       # (original Sentence, Processed sentece, predicted Sentence, 
#       # refTime (epoch), predictedBeginTimestring (mm/dd/yyyy %H:%m:%s) , predictedEndTimestring (mm/dd/yyyy %H:%m:%s))
#     predictedResults = dataParser.loadTranslateUnlabeledData(testInputFile, outputTestFile)
#     utils.print_ds(predictedResults)
#     
    
if __name__ == "__main__":
    main()