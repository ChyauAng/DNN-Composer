import os
from Preprocess import DataPreprocess
from Preprocess import MergeABCfiles

#MergeABCfiles Tester
#done
dir_name = 'C:\\Users\Anamnesis\\Documents\\Aptana Studio 3 Workspace\\DNN_Composer\\dataset'
data = []
Temp = MergeABCfiles.MergeFiles(dir_name, data)
Temp.main()


#Pitch Tester
#done
dataPreprocessor = DataPreprocess.ABCPreprocess(dir_name, data)
file_name = 'dataset.dat'
pitch = dataPreprocessor.getPitch(file_name)

file_object = open('pitch.dat', 'w')

for i in range(len(pitch)):
    file_object.writelines(pitch[i].__str__() + '\n')


#Duration Tester 
#done
duration = dataPreprocessor.getDuration(file_name)

file_object = open('duration.dat', 'w')
for i in range(len(duration)):
    file_object.writelines(duration[i].__str__() + '\n')
    
file_object.close()


