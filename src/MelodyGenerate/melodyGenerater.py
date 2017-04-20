from MelodyGenerate import getData
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.layers import GRU, Bidirectional, LSTM
from keras.optimizers import SGD, Adam  
import numpy as np
import os
import copy
from Preprocess import globalConstant as G

class MelodyGenerate:
    """
    Generate melody using GRU-RNN(GNN).
    """
    
    def _init_(self):
        
        self.rhythm = Sequential()
        self.melody = Sequential()
        
#         These variables cost too much memory. 
#         self.pitch_train = []
#         self.duration_train = []
#         self.pitch_test = []
#         self.duration_test = []
#         
        self.melody_train = []
        self.rhythm_train = []
        self.melody_train_labels = []
        self.rhythm_train_labels = []
         
        self.melody_test = []
        self.rhythm_test = []
        self.melody_test_labels = []
        self.rhythm_test_labels = []
        
        self.pitch_generate = []
        self.duration_generate = []
        
        self.batch_size = 128  #to be changed
        self.nb_epoch = 1 #to be changed
        self.data_dim = 56  #23-dimension plus 33-dimension
        self.train_timesteps = 1
        self.test_timesteps = 1
        
        self.timestep = 1
        
    def getData(self, timestep):
        """
        Get the rhythm batch size.
        Prepare the melody and rhythm arrays to be the input of the model.
        """
        
        self._init_()
        self.timestep = timestep
        
        getDataor = getData.getData()
        
        #padding the senquence
        temp = 0
        G.pitch_train, self.train_timesteps = getDataor.padSequences(G.pitch_train, 33)
        G.pitch_test, self.test_timesteps = getDataor.padSequences(G.pitch_test, 33)
        G.duration_train, temp = getDataor.padSequences(G.duration_train, 23)
        G.duration_test, temp= getDataor.padSequences(G.duration_test, 23)
        
        difference = self.train_timesteps - self.test_timesteps
        if difference < 0:
            G.pitch_train, G.duration_train = getDataor.trainTimestepsNormalization(difference, G.pitch_train, G.duration_train)
        elif difference > 0:
            G.pitch_test, G.duration_test = getDataor.testTimestepsNormalization(difference, G.pitch_test, G.duration_test)
        else:
            pass
        
        
#         pitch_train = getDataor.getPitch(pitch_train_file_name)
#         duration_train = getDataor.getDuration(duration_train_file_name)
#         
#         pitch_test = getDataor.getPitch(pitch_test_file_name)
#         duration_test = getDataor.getDuration(duration_test_file_name)
        
        melody_train, rhythm_train, melody_train_labels, rhythm_train_labels = getDataor.getMelodyRhythm(G.pitch_train, G.duration_train, 
                                                                                                         timestep, int(max(self.train_timesteps, self.test_timesteps) / timestep))
        
        melody_test, rhythm_test, melody_test_labels, rhythm_test_labels = getDataor.getMelodyRhythm(G.pitch_test, G.duration_test, 
                                                                                                     timestep, int(max(self.train_timesteps, self.test_timesteps) / timestep))
        
#         print(melody_train, melody_train[10])
        
#         melody_train_labels, rhythm_train_labels = getDataor.getLabels(melody_train, 
#                                                                         rhythm_train)
#         melody_test_labels, rhythm_test_labels = getDataor.getLabels(melody_test, 
#                                                                         rhythm_test)
        
        self.melody_train = np.array(melody_train)
        self.rhythm_train = np.array(rhythm_train)
        self.melody_train_labels = np.array(melody_train_labels)
        self.rhythm_train_labels = np.array(rhythm_train_labels)
        self.melody_test = np.array(melody_test)
        self.rhythm_test = np.array(rhythm_test)
        self.melody_test_labels = np.array(melody_test_labels) 
        self.rhythm_test_labels = np.array(rhythm_test_labels) 
        
        
           
           
    def modelConstruction(self):
        """
        Construct the melody and rhythm model.
        """
#         self.melody.add(GRU(128, consume_less = 'mem', return_sequences = True,
#                            input_shape = (self.timestep, 56)))
# #         self.melody.add(Dropout(0.5))
#         self.rhythm.add(GRU(128, consume_less = 'mem', return_sequences = True,
#                            input_shape = (self.timestep, 56)))
#         self.rhythm.add(Dropout(0.5))
#           
#         for i in range(2):
#             self.melody.add(GRU(128, return_sequences = True))
# #             self.melody.add(Dropout(0.5))
#             self.rhythm.add(GRU(128, return_sequences = True))
#             self.rhythm.add(Dropout(0.5))

        self.melody.add(Dense(128, input_shape = (self.timestep, 56)))
        self.rhythm.add(Dense(128, input_shape = (self.timestep, 56)))
           
        for i in range(4):
            self.melody.add(Bidirectional(LSTM(128, return_sequences = True)))
            self.melody.add(Dropout(0.5))
            self.rhythm.add(GRU(128, return_sequences = True))
#             self.rhythm.add(Dropout(0.5))    

        self.melody.add(Dense(128, input_shape = (self.timestep, 56)))
        self.rhythm.add(Dense(128, input_shape = (self.timestep, 56)))
           
#         for i in range(3):
#             self.melody.add(Bidirectional(GRU(128, return_sequences = True)))
#             self.melody.add(Dropout(0.5))
#             self.rhythm.add(GRU(128, return_sequences = True))        
            
    
        self.melody.add(Dense(33, activation = 'softmax'))
        self.rhythm.add(Dense(23, activation = 'softmax'))

        
        #compile part
        self.melody.compile(optimizer = 'adam',
                            #loss = self.my_loss_function()
                            loss = 'categorical_crossentropy')
        self.rhythm.compile(optimizer = 'adam',
                            #loss = self.my_loss_function()
                            loss = 'categorical_crossentropy')

        
        
    def trainProcess(self):
        """
        Start training the model.
        Remember the difference between the input of the melody and rhythm model. 
        """
        
        self.melody.fit(self.melody_train, self.melody_train_labels, batch_size = self.batch_size, nb_epoch = self.nb_epoch)        
        self.rhythm.fit(self.rhythm_train, self.rhythm_train_labels, batch_size = self.batch_size, nb_epoch = self.nb_epoch)

    def evaluateProcess(self):
        score_melody = self.melody.evaluate(self.melody_test, self.melody_test_labels, batch_size = self.batch_size)
        score_rhythm = self.rhythm.evaluate(self.rhythm_test, self.rhythm_test_labels, batch_size = self.batch_size)
        
        print('The test error of melody is', score_melody)
        print('The test error of rhythm is', score_rhythm)
        
        
    #need be fixed
    def generater(self, length, pitch_index, duration_index):
        """
        The generater to generate new melody and rhythm.
        Rhythm first and Melody next.
        """
        
        melody_x = np.zeros((1, self.timestep, 56))
        rhythm_x = np.zeros((1, self.timestep, 56))
        
        next_duration_index = [[0] * self.timestep]
        next_pitch_index = [[0] * self.timestep]
        
        for i in range(self.timestep):
            melody_x[0][i][pitch_index[i]] = 1

            rhythm_x[0][i][pitch_index[i]] = 1
            rhythm_x[0][i][duration_index[i] + 33] = 1

        for i in range(self.timestep):
            self.pitch_generate.append(list(rhythm_x[0][i][0 : 33]))
            self.duration_generate.append(list(rhythm_x[0][i][33 : 56]))
        
        
        for i in range(length):
            
            preds_rhythm = self.rhythm.predict(rhythm_x, verbose=0)
            print(preds_rhythm)
            
            for j in range(self.timestep):
                next_duration_index[0][j] = self.getIndex(preds_rhythm[0, j], 23)
                next_duration_index[0][j] = next_duration_index[0][j] + 33
            
            for j in range(self.timestep):
                melody_x[0][j][next_duration_index[0][j]] = 1
            preds_melody = self.melody.predict(melody_x, verbose=0)
            
            for j in range(self.timestep):
                next_pitch_index[0][j] = self.getIndex(preds_melody[0, j], 33)
            
            
            print(preds_melody.shape)
            print(preds_rhythm.shape)
            
            
            next_melody_x = np.zeros((1, self.timestep, 56))
            next_rhythm_x = np.zeros((1, self.timestep, 56))
            
            for j in range(self.timestep):
                next_melody_x[0][j][next_pitch_index[0][j]] = 1

                next_rhythm_x[0][j][next_pitch_index[0][j]] = 1
                next_rhythm_x[0][j][next_duration_index[0][j]] = 1
            
            for j in range(self.timestep):
                self.pitch_generate.append(list(next_rhythm_x[0][j][0 : 33]))
                self.duration_generate.append(list(next_rhythm_x[0][j][33 : 56]))
            
            melody_x = copy.deepcopy(next_melody_x)
            rhythm_x = copy.deepcopy(next_rhythm_x)
            
        return self.pitch_generate, self.duration_generate
    
    def getIndex(self, list, length):
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
    
            
    def abcFileWriter(self, pitch, duration, file_name):
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
        for i in range(int(len(pitch) / self.timestep)):
            for j in range(self.timestep):
                pitch_index = pitch[i * self.timestep + j].index(1)
                file.write(pitch_index_list[pitch_index].__str__())
                
                duration_index = duration[i * self.timestep + j].index(1)
                file.write(duration_index_list[duration_index].__str__())
                
                file.write(' ')
            file.write('|')
            
        file.write('|')
        file.close()    
        
    def saveModels(self):
        self.melody.save('melody.h5')
        self.rhythm.save('rhythm.h5')
            
                        