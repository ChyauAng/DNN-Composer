from keras.models import load_model
from Preprocess import GlobalConstant as G
import numpy as np
import copy

#load model
melody = load_model('melody.h5')
rhythm = load_model('rhythm.h5')

pitch_generate = []
duration_generate = []

#generate function
def generater(melody, rhythm, length, timestep, pitch_index, duration_index):
        """
        The generater to generate new melody and rhythm.
        Rhythm first and Melody next.
        """
        
        melody_x = np.zeros((1, timestep, 56))
        rhythm_x = np.zeros((1, timestep, 56))
        
        next_duration_index = [[0] * timestep]
        next_pitch_index = [[0] * timestep]
        
        for i in range(timestep):
            melody_x[0][i][pitch_index[i]] = 1

            rhythm_x[0][i][pitch_index[i]] = 1
            rhythm_x[0][i][duration_index[i] + 33] = 1

        for i in range(timestep):
            pitch_generate.append(list(rhythm_x[0][i][0 : 33]))
            duration_generate.append(list(rhythm_x[0][i][33 : 56]))
        
        
        for i in range(length):
            
            preds_rhythm = rhythm.predict(rhythm_x, verbose=0)
            print(preds_rhythm)
            
            for j in range(timestep):
                next_duration_index[0][j] = getIndex(preds_rhythm[0, j], 23)
                next_duration_index[0][j] = next_duration_index[0][j] + 33
            
            for j in range(timestep):
                melody_x[0][j][next_duration_index[0][j]] = 1
            preds_melody = melody.predict(melody_x, verbose=0)
            
            for j in range(timestep):
                next_pitch_index[0][j] = getIndex(preds_melody[0, j], 33)
            
            
            print(preds_melody.shape)
            print(preds_rhythm.shape)
            
            
            next_melody_x = np.zeros((1, timestep, 56))
            next_rhythm_x = np.zeros((1, timestep, 56))
            
            for j in range(timestep):
                next_melody_x[0][j][next_pitch_index[0][j]] = 1

                next_rhythm_x[0][j][next_pitch_index[0][j]] = 1
                next_rhythm_x[0][j][next_duration_index[0][j]] = 1
            
            for j in range(timestep):
                pitch_generate.append(list(next_rhythm_x[0][j][0 : 33]))
                duration_generate.append(list(next_rhythm_x[0][j][33 : 56]))
            
            melody_x = copy.deepcopy(next_melody_x)
            rhythm_x = copy.deepcopy(next_rhythm_x)
            
        return pitch_generate, duration_generate
    
def getIndex(list, length):
        """
        Get the index of the largest probability of the current pitch and duration.
        """
        maxIndex = 0
        maxValue = list[0]
        
        for i in range(length - 1):
            if(list[i + 1] > maxValue):
                maxIndex = i + 1
                maxValue = list[i + 1]
        
        return maxIndex

#write into abc files    
def abcFileWriter( pitch, duration, timestep, file_name):
        """
        Write pitch and duration in files.
        """
        pitch_index = 0
        duration_index = 0
        
        file = open(file_name, 'w')
        file.write('X:1\nT:Melody Generated\nM:6/8\nL:1/8\nK:C\n')
        duration_index_list = ['1/4', '1/3', '1/2', '3/4', '3/8', 
                               '5/8', '2/3', '2/5', '4/9', '4/5', 
                               '1',  '3/2', '4/3', '9/8', '2', 
                               '8/3', '9/4', '7/2', '3', '4', 
                               '9/2', '6', '8']
        
        pitch_index_list=['G,', '^G,', 'A,', '^A,', 'B,', 'C', '^C', 'D',
                          '^D', 'E', 'F', '^F', 'G', '^G', 'A', '^A',
                          'B', 'c', '^c', 'd', '^d', 'e', 'f', '^f',
                          'g', '^g', 'a', '^a', 'b', 'c\'', '^c\'', 'd\'', '^d\'']
        for i in range(int(len(pitch) / timestep)):
            for j in range(timestep):
                pitch_index = pitch[i * timestep + j].index(1)
                file.write(pitch_index_list[pitch_index].__str__())
                
                duration_index = duration[i * timestep + j].index(1)
                file.write(duration_index_list[duration_index].__str__())
                
                file.write(' ')
            file.write('|')
            
        file.write('|')
        file.close() 

#seed
timestep = 23
pitch_index = [16, 21, 21, 16, 14,
               16, 21, 21, 16, 14, 11,
               16, 21, 21, 16, 21, 21,
               16, 14, 11, 14, 11, 7]
duration_index = [10, 10, 10, 14, 10,
                  10, 10, 10, 10, 10, 10,
                  10, 10, 10, 10, 10, 10,
                  10, 10, 10, 10, 10, 10]

#generating process
pitch, duration =generater(melody, rhythm, 5, timestep, pitch_index, duration_index)

abcFileWriter(pitch, duration, timestep, 'generation.abc')