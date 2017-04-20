from MelodyGenerate import melodyGenerater
import numpy as np
                        
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
 

data = []
dataPreprocessor = dataPreprocess.ABCPreprocess(dir_name, data)    
pitch = dataPreprocessor.getPitch(file_name_test)
globalConstant.pitch_test = copy.deepcopy(pitch)

 
#Duration Tester 
#done
data = []
dataPreprocessor = dataPreprocess.ABCPreprocess(dir_name, data)
duration = dataPreprocessor.getDuration(file_name)
globalConstant.duration_train = copy.deepcopy(duration)
 
data = []
dataPreprocessor = dataPreprocess.ABCPreprocess(dir_name, data)
duration = dataPreprocessor.getDuration(file_name_test)
globalConstant.duration_test = copy.deepcopy(duration)


     
     
# file_object.close()                        
generator = melodyGenerater.MelodyGenerate()
# generator.getData(10)

#seed0
# generator.getData(23)
#seed1
# generator.getData(24)
#seed2
generator.getData(15)



# file_object = open('pitch_train.dat', 'w')
# for i in range(len(globalConstant.pitch_train)):
#     file_object.writelines(globalConstant.pitch_train[i].__str__() + '\n')
#  
# file_object = open('pitch_test.dat', 'w')
# for i in range(len(globalConstant.pitch_test)):
#     file_object.writelines(globalConstant.pitch_test[i].__str__() + '\n')
#  
# file_object = open('duration_train.dat', 'w')
# for i in range(len(globalConstant.duration_train)):
#     file_object.writelines(globalConstant.duration_train[i].__str__() + '\n')
#  
# file_object = open('duration_test.dat', 'w')
# for i in range(len(globalConstant.duration_test)):
#     file_object.writelines(globalConstant.duration_test[i].__str__() + '\n')

generator.modelConstruction()
generator.trainProcess()
generator.evaluateProcess()
# generator.saveModels()


# pitch_index = [9, 9, 9, 14, 14, 12, 12, 9, 5, 7]
# duration_index = [10, 14, 10, 14, 10, 14, 10, 14, 10, 14]
 
# pitch_index = [12, 15, 15, 14, 12, 10, 14, 17]
# duration_index = [11, 2, 14, 11, 2, 14, 11, 2]
 
# pitch_index = [16, 21, 21, 16, 14,
#                16, 21, 21, 16, 14, 11,
#                16, 21, 21, 16, 21, 21,
#                16, 14, 11, 14, 11, 7]
# duration_index = [10, 10, 10, 14, 10,
#                   10, 10, 10, 10, 10, 10,
#                   10, 10, 10, 10, 10, 10,
#                   10, 10, 10, 10, 10, 10]

pitch_index = [9, 14, 9, 13, 14, 16, 18, 14, 21, 21, 19, 18, 14, 14, 11]
duration_index = [14, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]

# pitch, duration =generator.generater(5, pitch_index, duration_index)
#  
# generator.abcFileWriter(pitch, duration, 'generation.abc')

# pitch_index = [16, 21, 21, 23, 21, 21,
#                26, 21, 21, 23, 21, 19,
#                16, 21, 21, 23, 21, 21,
#                23, 26, 24, 23, 21, 19]
# duration_index = [10, 10, 10, 10, 10, 10,
#                   10, 10, 10, 10, 10, 10,
#                   10, 10, 10, 10, 10, 10, 
#                   10, 10, 10, 10, 10, 10,]
pitch, duration =generator.generater(3, pitch_index, duration_index)
  
generator.abcFileWriter(pitch, duration, 'generation_seed.abc')





