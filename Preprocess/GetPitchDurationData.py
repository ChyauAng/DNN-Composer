import os
from Preprocess import DataPreprocess
from Preprocess import MergeABCfiles

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
Temp1 = MergeABCfiles.MergeFiles(dir_name_train, data)
Temp1.main('train_set.dat')

data = []
Temp2 = MergeABCfiles.MergeFiles(dir_name_test, data)
Temp2.main('test_set.dat') 


#Pitch Tester
#done

data = []
dataPreprocessor = DataPreprocess.ABCPreprocess(dir_name, data)

file_name = 'train_set.dat'
file_name_test = 'test_set.dat'

pitch = dataPreprocessor.getPitch(file_name)
file_object = open('pitch_train.dat', 'w')
for i in range(len(pitch)):
    file_object.writelines(pitch[i].__str__() + '\n')


data = []
dataPreprocessor = DataPreprocess.ABCPreprocess(dir_name, data)    
pitch = dataPreprocessor.getPitch(file_name_test)
file_object = open('pitch_test.dat', 'w')
for i in range(len(pitch)):
    file_object.writelines(pitch[i].__str__() + '\n')


#Duration Tester 
#done
data = []
dataPreprocessor = DataPreprocess.ABCPreprocess(dir_name, data)
duration = dataPreprocessor.getDuration(file_name)
file_object = open('duration_train.dat', 'w')
for i in range(len(duration)):
    file_object.writelines(duration[i].__str__() + '\n')

data = []
dataPreprocessor = DataPreprocess.ABCPreprocess(dir_name, data)
duration = dataPreprocessor.getDuration(file_name_test)
file_object = open('duration_test.dat', 'w')
for i in range(len(duration)):
    file_object.writelines(duration[i].__str__() + '\n')
    
    
file_object.close()



