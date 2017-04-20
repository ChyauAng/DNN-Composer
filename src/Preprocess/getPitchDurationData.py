import os
import copy
from Preprocess import dataPreprocess
from Preprocess import filesProcessor
from Preprocess import globalConstant

"""
The total number of songs in the data set is 2315.
The number of songs used to be trained is 1571.
The number of songs used to be tested is 744.

The number of vectors to be trained is 235141 * 2.
The number of vectors to be tested is 112461 * 2.

"""
dir_name = os.path.join('..', 'dataset')
dir_name_train = os.path.join('..', 'dataset', 'train')
dir_name_test = os.path.join('..', 'dataset', 'test')

#MergeABCfiles Tester
#done


data = []
Temp1 = filesProcessor.FilesProcess(dir_name_train, data)
Temp1.main('train_set.dat')
Temp1.plusEnding('train_set.dat')

data = []
Temp2 = filesProcessor.FilesProcess(dir_name_test, data)
Temp2.main('test_set.dat') 
Temp2.plusEnding('test_set.dat')




#Pitch Tester
#done
 
data = []
dataPreprocessor = dataPreprocess.ABCPreprocess(dir_name, data)
 
file_name = 'train_set.dat'
file_name_test = 'test_set.dat'
 
pitch = dataPreprocessor.getPitch(file_name)
globalConstant.pitch_train = copy.deepcopy(pitch)
# file_object = open('pitch_train.dat', 'w')
# for i in range(len(pitch)):
#     file_object.writelines(pitch[i].__str__() + '\n')
 
 
data = []
dataPreprocessor = dataPreprocess.ABCPreprocess(dir_name, data)    
pitch = dataPreprocessor.getPitch(file_name_test)
globalConstant.pitch_test = copy.deepcopy(pitch)
# file_object = open('pitch_test.dat', 'w')
# for i in range(len(pitch)):
#     file_object.writelines(pitch[i].__str__() + '\n')
 
 
#Duration Tester 
#done
data = []
dataPreprocessor = dataPreprocess.ABCPreprocess(dir_name, data)
duration = dataPreprocessor.getDuration(file_name)
globalConstant.duration_train = copy.deepcopy(duration)
# file_object = open('duration_train.dat', 'w')
# for i in range(len(duration)):
#     file_object.writelines(duration[i].__str__() + '\n')
 
data = []
dataPreprocessor = dataPreprocess.ABCPreprocess(dir_name, data)
duration = dataPreprocessor.getDuration(file_name_test)
globalConstant.duration_test = copy.deepcopy(duration)
# file_object = open('duration_test.dat', 'w')
# for i in range(len(duration)):
#     file_object.writelines(duration[i].__str__() + '\n')
     
     
# file_object.close()



