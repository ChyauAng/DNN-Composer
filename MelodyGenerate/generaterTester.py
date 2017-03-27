from MelodyGenerate import MelodyGenerater
import numpy as np
                        
import os
import copy
from Preprocess import DataPreprocess
from Preprocess import filesProcessor
from Preprocess import GlobalConstant

"""
The total number of songs in the data set is 2315.
The number of songs used to be trained is 1571.
The number of songs used to be tested is 744.

The number of vectors to be trained is 235141 * 2.
The number of vectors to be tested is 112461 * 2.

"""
dir_name = '..\\dataset'
dir_name_train = '..\\dataset\\train'
dir_name_test = '..\\dataset\\test'

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
dataPreprocessor = DataPreprocess.ABCPreprocess(dir_name, data)
 
file_name = 'train_set.dat'
file_name_test = 'test_set.dat'
 
pitch = dataPreprocessor.getPitch(file_name)
GlobalConstant.pitch_train = copy.deepcopy(pitch)
# file_object = open('pitch_train.dat', 'w')
# for i in range(len(pitch)):
#     file_object.writelines(pitch[i].__str__() + '\n')
 
 
data = []
dataPreprocessor = DataPreprocess.ABCPreprocess(dir_name, data)    
pitch = dataPreprocessor.getPitch(file_name_test)
GlobalConstant.pitch_test = copy.deepcopy(pitch)
# file_object = open('pitch_test.dat', 'w')
# for i in range(len(pitch)):
#     file_object.writelines(pitch[i].__str__() + '\n')
 
 
#Duration Tester 
#done
data = []
dataPreprocessor = DataPreprocess.ABCPreprocess(dir_name, data)
duration = dataPreprocessor.getDuration(file_name)
GlobalConstant.duration_train = copy.deepcopy(duration)
# file_object = open('duration_train.dat', 'w')
# for i in range(len(duration)):
#     file_object.writelines(duration[i].__str__() + '\n')
 
data = []
dataPreprocessor = DataPreprocess.ABCPreprocess(dir_name, data)
duration = dataPreprocessor.getDuration(file_name_test)
GlobalConstant.duration_test = copy.deepcopy(duration)


     
     
# file_object.close()                        
generator = MelodyGenerater.MelodyGenerate()
generator.getData(10)

file_object = open('pitch_train.dat', 'w')
for i in range(len(GlobalConstant.pitch_train)):
    file_object.writelines(GlobalConstant.pitch_train[i].__str__() + '\n')
 
file_object = open('pitch_test.dat', 'w')
for i in range(len(GlobalConstant.pitch_test)):
    file_object.writelines(GlobalConstant.pitch_test[i].__str__() + '\n')
 
file_object = open('duration_train.dat', 'w')
for i in range(len(GlobalConstant.duration_train)):
    file_object.writelines(GlobalConstant.duration_train[i].__str__() + '\n')
 
file_object = open('duration_test.dat', 'w')
for i in range(len(GlobalConstant.duration_test)):
    file_object.writelines(GlobalConstant.duration_test[i].__str__() + '\n')

generator.modelConstruction()
generator.trainProcess()
generator.evaluateProcess()


pitch_index = [9, 9, 9, 14, 14, 12, 12, 9, 5, 7]
duration_index = [10, 14, 10, 14, 10, 14, 10, 14, 10, 14]
pitch, duration =generator.generater(50, pitch_index, duration_index)

generator.filesWriter(pitch, duration, 'pitch_generation.dat', 'duration_generation.dat')

generator.saveModels()


