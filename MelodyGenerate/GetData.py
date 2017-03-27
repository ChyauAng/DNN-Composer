import os
import numpy as np
import re
from Preprocess import GlobalConstant as G

class getData(object):
    """
    get the pitch and the duration to be trained.

    Properties
    ----------
    None.
    """
    
    def __init__(self):
        """
        Do the initialization work.
        """
        pass

    def padSequences(self, lists, length):
        max_timesteps = 0
        for i in range(len(lists)):
            if len(lists[i]) > max_timesteps:
                max_timesteps = len(lists[i])
#                 print(max_timesteps)
#                 print(len(lists))
#                 print(lists[i])
        
        for i in range(len(lists)):
            for j in range(max_timesteps - len(lists[i])):
                lists[i].append([0] * length)
    
        return lists, max_timesteps
    
    def trainTimestepsNormalization(self, difference, pitch_train, duration_train):
        difference = - difference
        
        for i in range(len(pitch_train)):
            for j in range(difference):
                pitch_train[i].append([0] * 33)
                
        for i in range(len(duration_train)):
            for j in range(difference):
                duration_train[i].append([0] * 23)
        
        return pitch_train, duration_train
    
    def testTimestepsNormalization(self, difference, pitch_test, duration_test):
        
        for i in range(len(pitch_test)):
            for j in range(difference):
                pitch_test[i].append([0] * 33)
                
        for i in range(len(duration_test)):
            for j in range(difference):
                duration_test[i].append([0] * 23)
                
        return pitch_test, duration_test
        
    
    def getMelodyRhythm(self, pitch, duration, timestep, steps_number):
        """
        Get the melody and the rhythm.
        The label of the current p[i] + d[i+1] of melody is p[i+1]
        The label of the current p[i] + d[i] of rhythm is d[i+1]
        Given that the dimensions of input and output can be different. 
        """
        
        melody = []
        rhythm = []
        melody_labels = []
        rhythm_labels = []
        
        melody_timesteps = []
        rhythm_timesteps = []
        melody_labels_timesteps = []
        rhythm_labels_timesteps = []
              
        for i in range(len(pitch)):
            for k in range(steps_number):
                for j in range(timestep):
  
                    rhythm_timesteps.append(pitch[i][k * timestep + j] + duration[i][k * timestep + j])
                        
                if i != (len(pitch) - 5):
                    for j in range(timestep):
                        melody_timesteps.append(pitch[i][k * timestep + j] + duration[i][k * timestep + j + 1])
                    
                    for j in range(timestep):
                        melody_labels_timesteps.append(pitch[i][k * timestep + j + 1])
  
                    
                    for j in range(timestep):
                            rhythm_labels_timesteps.append(duration[i][k * timestep + j + 1])

                else:
                    for j in range(timestep):
                        melody_timesteps.append([0] * 56)
                        melody_labels_timesteps.append([0] * 33)
                        rhythm_labels_timesteps.append([0] * 23)
                                   

                print(len(melody_timesteps))
            
                melody.append(melody_timesteps)
                rhythm.append(rhythm_timesteps)
                melody_labels.append(melody_labels_timesteps)
                rhythm_labels.append(rhythm_labels_timesteps)
            
                melody_timesteps = []
                rhythm_timesteps = []
                melody_labels_timesteps = []
                rhythm_labels_timesteps = []
            
#         for i in range(len(pitch)):
#             for j in range(timestep):
#   
#                 rhythm_timesteps.append(pitch[i][i * steps_number + j] + duration[i][i * steps_number + j])
#                         
#             if i != (num - 5):
#                 for j in range(timestep):
#                     melody_timesteps.append(pitch[i][i * steps_number + j] + duration[i][i * steps_number + j + 1])
#                     
#                 for j in range(timestep):
#                     melody_labels_timesteps.append(pitch[i][i * steps_number + j + 1])
#   
#                     
#                 for j in range(timestep):
#                         rhythm_labels_timesteps.append(duration[i][i * steps_number + j + 1])
# 
#                 else:
#                     for j in range(timestep):
#                         melody_timesteps.append([0] * 56)
#                         melody_labels_timesteps.append([0] * 33)
#                         rhythm_labels_timesteps.append([0] * 23)
#                                    
# 
#             melody.append(melody_timesteps)
#             rhythm.append(rhythm_timesteps)
#             melody_labels.append(melody_labels_timesteps)
#             rhythm_labels.append(rhythm_labels_timesteps)
#             
#             melody_timesteps = []
#             rhythm_timesteps = []
#             melody_labels_timesteps = []
#             rhythm_labels_timesteps = []
            

                   
        return melody, rhythm, melody_labels, rhythm_labels
        
