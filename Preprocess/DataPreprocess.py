#data preprocessor extracting pitch and duration information from abc files  

import os
import re
import numpy as np
from Preprocess import ABCParser
from Preprocess import GlobalConstant

class ABCPreprocess:
    """
    Preprocess and extract the pitch and duration information from ABC notation files. 

    Properties
    ----------
    measure
        An array of measure information, as measure objects.
    pitch
        A two dimension array of pitch information, as arrays of 34 dimension arrays representing the pitch of each note.
    pitch_dictionary
        A dictionary whose keys are notes and values are indexes of the pitch of each note .
    duration
        A two dimension array of pitch information, as arrays of 23 dimension arrays representing the duration of each note.
    duration_dictionary
        A dictionary whose keys are duration and values are indexes of the duration of each note .
    dir_path
        The path of the directory.
    data
        The ABC files information.
    """
    
    def __init__(self, dir_path, data=[]):
        """
        Do the initialization work.
        """
        self.measures = [] #measure information
        self.pitch = []    # pitch information
        #transpose the key of every song to C Major
        #key must be unchangable, so use 34 as the never reachable index
        #not nessary assign value by such a clumsy way. while the clumy way also has its advantages...  
        self.pitch_dictionary = {GlobalConstant.note[0] : 0, GlobalConstant.note[1] : 1, GlobalConstant.note[2] : 34, GlobalConstant.note[3] : 0,
                                GlobalConstant.note[4] : 2, GlobalConstant.note[5] : 3, GlobalConstant.note[6] : 1, GlobalConstant.note[7] : 2,
                                GlobalConstant.note[8] : 4, GlobalConstant.note[9] : 5, GlobalConstant.note[10] : 3, GlobalConstant.note[11] : 4,
                                GlobalConstant.note[12] : 5, GlobalConstant.note[13] : 6, GlobalConstant.note[14] : 4, GlobalConstant.note[15] : 5,
                                GlobalConstant.note[16] : 7, GlobalConstant.note[17] : 8, GlobalConstant.note[18] : 6, GlobalConstant.note[19] : 7,
                                GlobalConstant.note[20] : 9, GlobalConstant.note[21] : 10, GlobalConstant.note[22] : 8, GlobalConstant.note[23] : 9,
                                GlobalConstant.note[24] : 10, GlobalConstant.note[25] : 11, GlobalConstant.note[26] : 9, GlobalConstant.note[27] : 10,
                                GlobalConstant.note[28] : 12, GlobalConstant.note[29] : 13, GlobalConstant.note[30] : 11, GlobalConstant.note[31] : 12,
                                GlobalConstant.note[32] : 14, GlobalConstant.note[33] : 15, GlobalConstant.note[34] : 13, GlobalConstant.note[35] : 14,
                                GlobalConstant.note[36] : 16, GlobalConstant.note[37] : 17, GlobalConstant.note[38] : 15, GlobalConstant.note[39] : 16,
                                GlobalConstant.note[40] : 17, GlobalConstant.note[41] : 18, GlobalConstant.note[42] : 16, GlobalConstant.note[43] : 17,
                                GlobalConstant.note[44] : 19, GlobalConstant.note[45] : 20, GlobalConstant.note[46] : 18, GlobalConstant.note[47] : 19,
                                GlobalConstant.note[48] : 21, GlobalConstant.note[49] : 22, GlobalConstant.note[50] : 20, GlobalConstant.note[51] : 21,
                                GlobalConstant.note[52] : 22, GlobalConstant.note[53] : 23, GlobalConstant.note[54] : 21, GlobalConstant.note[55] : 22,
                                GlobalConstant.note[56] : 24, GlobalConstant.note[57] : 25, GlobalConstant.note[58] : 23, GlobalConstant.note[59] : 24,
                                GlobalConstant.note[60] : 26, GlobalConstant.note[61] : 27, GlobalConstant.note[62] : 25, GlobalConstant.note[63] : 26,
                                GlobalConstant.note[64] : 28, GlobalConstant.note[65] : 29, GlobalConstant.note[66] : 27, GlobalConstant.note[67] : 28,
                                GlobalConstant.note[68] : 29, GlobalConstant.note[69] : 30, GlobalConstant.note[70] : 28, GlobalConstant.note[71] : 29,
                                GlobalConstant.note[72] : 31, GlobalConstant.note[73] : 32, GlobalConstant.note[74] : 30, GlobalConstant.note[75] : 31}

                                
        #list first, then convert it to numpy array. see ListToNumpyArrayTest.py.
        self.duration = []    # duration information
            
        self.duration_dictionary = {GlobalConstant.index0 : 0, 
                                    GlobalConstant.index1 : 1,
                                    GlobalConstant.index2 : 2,
                                    GlobalConstant.index3 : 3,
                                    GlobalConstant.index4 : 4,
                                    GlobalConstant.index5 : 5, 
                                    GlobalConstant.index6 : 6,
                                    GlobalConstant.index7 : 7,
                                    GlobalConstant.index8 : 8,
                                    GlobalConstant.index9 : 9,
                                    GlobalConstant.index10 : 10,
                                    GlobalConstant.index11 : 11,
                                    GlobalConstant.index12 : 12,
                                    GlobalConstant.index13 : 13,
                                    GlobalConstant.index14 : 14,
                                    GlobalConstant.index15 : 15,
                                    GlobalConstant.index16 : 16,
                                    GlobalConstant.index17 : 17,
                                    GlobalConstant.index18 : 18,
                                    GlobalConstant.index19 : 19,
                                    GlobalConstant.index20 : 20,
                                    GlobalConstant.index21 : 21,
                                    GlobalConstant.index22 : 22                                 
                                    }
        self.dir_path = dir_path;    #path of directionary
        self.data = data    #ABC files information
            
    def processFolder(self, file_name):
        """
        Concatenate all lines from all files in dir_path and return a list.
        """
 
        files = []
        self.listdir(self.dir_path, files)
        for file in files:         
            if file.split('.')[-1] == 'abc': # Only open abc files
                with open(file, 'r') as f:
                    lines = f.readlines()
                    # Skip header info
                    i = 0
                    init = lines[i][0:2]
                    while init != 'X:':
                        i += 1
                        try:
                            init = lines[i][0:2]
                        except:
                            i -= 1
                            break
                    self.data += lines[i:]
        
        file_object = open(file_name, 'w')
        file_object.writelines(self.data)
        file_object.close()
        
        #return data
    
    
    def listdir(self, dir_path, files):
        """
        Handle the dataset directionary recursively
        """
        
        for item in os.listdir(dir_path):
            if os.path.isdir(os.path.join(dir_path, item)):
                self.listdir(os.path.join(dir_path, item),files)   
            else:
                files.append(os.path.join(dir_path, item))
        
    
    def keyNormalization(self, file_name):
        """
        Transpose the key of every song to C Major
        """
        
        #song is a 2-dimension array carrying the information of every song
        song = [[] for i in range(2317)]
        text = []
        raw_line = []
        key = ''
        flag =True
        
        file = open(file_name, 'Ur')
        text = file.readlines()
        file.close()
        
        #print(text)
        
        song_count = -1
        for line in text:
            line = re.sub('\n', '', line)
            if re.search('X:[0-9]+', line) != None:
                song_count = song_count + 1
            song[song_count].append(line)
        
        #operate every song
        for i in range(2317):
            for every_line in song[i]:
                if re.search('K:[A-Z][a-z]*', every_line) != None:
                    #get key value
                    key = re.sub('K:', '', every_line)
                    key = re.sub('\n', '', key)
                    flag =False
                    
#                     print(key)
#                     print(len(key))
                    
                    #every_line = every_line.replace('K:', '')
                elif re.search('(([A-J]|[L-Z]):[A-Z]*[a-z]*)', every_line) != None:
                    flag =False
                    
                else:
                    flag = True
                          
                    #A
                    if key == 'Am':
                        pass
                    elif key == 'A':
                        every_line = re.sub('C', '^C', every_line)
                        every_line = re.sub('F', '^F', every_line)
                        every_line = re.sub('G', '^G', every_line)
                        
                        every_line = re.sub('c', '^c', every_line)
                        every_line = re.sub('f', '^f', every_line)
                        every_line = re.sub('g', '^g', every_line)
                    elif key == 'Amix':
                        every_line = re.sub('F', '^F', every_line, re.IGNORECASE)
                        every_line = re.sub('f', '^f', every_line, re.IGNORECASE)
                    elif key == 'Ador':
                        every_line = re.sub('C', '^C', every_line)
                        every_line = re.sub('F', '^F', every_line)
                        
                        every_line = re.sub('c', '^c', every_line)
                        every_line = re.sub('f', '^f', every_line)
                    #B
                    elif key == 'B':
                        every_line = re.sub('C', '^C', every_line)
                        every_line = re.sub('D', '^D', every_line)
                        every_line = re.sub('F', '^F', every_line)
                        every_line = re.sub('G', '^G', every_line)
                        every_line = re.sub('A', '^A', every_line)
                        
                        every_line = re.sub('c', '^c', every_line)
                        every_line = re.sub('d', '^d', every_line)
                        every_line = re.sub('f', '^f', every_line)
                        every_line = re.sub('g', '^g', every_line)
                        every_line = re.sub('a', '^a', every_line)
                    elif key == 'Bm':
                        every_line = re.sub('C', '^C', every_line)
                        every_line = re.sub('F', '^F', every_line)
                        
                        every_line = re.sub('c', '^c', every_line)
                        every_line = re.sub('f', '^f', every_line)
                    elif key == 'Bmix':
                        every_line = re.sub('C', '^C', every_line)
                        every_line = re.sub('D', '^D', every_line)
                        every_line = re.sub('F', '^F', every_line)
                        every_line = re.sub('G', '^G', every_line)
                        
                        every_line = re.sub('c', '^c', every_line)
                        every_line = re.sub('d', '^d', every_line)
                        every_line = re.sub('f', '^f', every_line)
                        every_line = re.sub('g', '^g', every_line)
                    elif key == 'Bdor':
                        every_line = re.sub('C', '^C', every_line)
                        every_line = re.sub('F', '^F', every_line)
                        every_line = re.sub('G', '^G', every_line)
                        
                        every_line = re.sub('c', '^c', every_line)
                        every_line = re.sub('f', '^f', every_line)
                        every_line = re.sub('g', '^g', every_line)
                    #C
                    elif key == 'C':
                        pass
                    elif key == 'Cm':
                        every_line = re.sub('E', '_E', every_line)
                        every_line = re.sub('A', '_A', every_line)
                        every_line = re.sub('B', '_B', every_line)
                        
                        every_line = re.sub('e', '_e', every_line)
                        every_line = re.sub('a', '_a', every_line)
                        every_line = re.sub('b', '_b', every_line)
                    elif key == 'Cmix':
                        every_line = re.sub('B', '_B', every_line)
                        every_line = re.sub('b', '_b', every_line)
                    elif key == 'Cdor':
                        every_line = re.sub('E', '_E', every_line)
                        every_line = re.sub('B', '_B', every_line)
                        
                        every_line = re.sub('e', '_e', every_line)
                        every_line = re.sub('b', '_b', every_line)
                    #D
                    elif key == 'D':
                        every_line = re.sub('C', '^C', every_line)
                        every_line = re.sub('F', '^F', every_line)
                        
                        every_line = re.sub('c', '^c', every_line)
                        every_line = re.sub('f', '^f', every_line)
                    elif key == 'Dm':
                        every_line = re.sub('B', '_B', every_line)
                        every_line = re.sub('b', '_b', every_line)
                    elif key == 'Dmix':
                        every_line = re.sub('F', '^F', every_line)
                        every_line = re.sub('f', '^f', every_line)
                    elif key == 'Ddor':
                        pass
                    #E
                    elif key == 'E':
                        every_line = re.sub('C', '^C', every_line)
                        every_line = re.sub('D', '^D', every_line)
                        every_line = re.sub('F', '^F', every_line)
                        every_line = re.sub('G', '^G', every_line)
                        
                        every_line = re.sub('c', '^c', every_line)
                        every_line = re.sub('d', '^d', every_line)
                        every_line = re.sub('f', '^f', every_line)
                        every_line = re.sub('g', '^g', every_line)
                    elif key == 'Em':
                        every_line = re.sub('F', '^F', every_line)
                        every_line = re.sub('f', '^f', every_line)
                    elif key == 'Emix':
                        every_line = re.sub('C', '^C', every_line)
                        every_line = re.sub('F', '^F', every_line)
                        every_line = re.sub('G', '^G', every_line)
                        
                        every_line = re.sub('c', '^c', every_line)
                        every_line = re.sub('f', '^f', every_line)
                        every_line = re.sub('g', '^g', every_line)
                    elif key == 'Edor':
                        every_line = re.sub('C', '^C', every_line)
                        every_line = re.sub('F', '^F', every_line)
                        
                        every_line = re.sub('c', '^c', every_line)
                        every_line = re.sub('f', '^f', every_line)
                    #F
                    elif key == 'F':
                        every_line = re.sub('B', '_B', every_line)
                        every_line = re.sub('b', '_b', every_line)
                    elif key == 'Fm':
                        every_line = re.sub('D', '_D', every_line)
                        every_line = re.sub('E', '_E', every_line)
                        every_line = re.sub('A', '_A', every_line)
                        every_line = re.sub('B', '_B', every_line)
                        
                        every_line = re.sub('d', '_d', every_line)
                        every_line = re.sub('e', '_e', every_line)
                        every_line = re.sub('a', '_a', every_line)
                        every_line = re.sub('b', '_b', every_line)
                    elif key == 'Fmix':
                        every_line = re.sub('E', '_E', every_line)
                        every_line = re.sub('B', '_B', every_line)
                        
                        every_line = re.sub('e', '_e', every_line)
                        every_line = re.sub('b', '_b', every_line)
                    elif key == 'Fdor':
                        every_line = re.sub('E', '_E', every_line)
                        every_line = re.sub('A', '_A', every_line)
                        every_line = re.sub('B', '_B', every_line)
                        
                        every_line = re.sub('e', '_e', every_line)
                        every_line = re.sub('a', '_a', every_line)
                        every_line = re.sub('b', '_b', every_line)
                    #G
                    elif key == 'G':
                        every_line = re.sub('F', '^F', every_line)
                        every_line = re.sub('f', '^f', every_line)
                    elif key == 'Gm':
                        every_line = re.sub('E', '_E', every_line)
                        every_line = re.sub('B', '_B', every_line)
                        
                        every_line = re.sub('e', '_e', every_line)
                        every_line = re.sub('b', '_b', every_line)
                    elif key == 'Gmix':
                        pass
                    elif key == 'Gdor':
                        every_line = re.sub('B', '_B', every_line)
                        every_line = re.sub('b', '_b', every_line)
                    #key error
                    else:
                        print(every_line)
                        print(key)
                        print("Key Error!!")
                        
                if flag == True:        
                    every_line = re.sub('=\^', '', every_line)
                    every_line = re.sub('=_', '', every_line)
                                               
                    raw_line.append(every_line)
                    
        return raw_line


    def getLines(self,file_name):
        """
        Get line information, return an array of line objects.
        """
        
        tune=ABCParser.Tune(file_name)
        #print(tune.line[0].measure)
        return tune.line
    
    
    def getMeasures(self, file_name):
        """
        Get measure information, return an array of measure objects.
        """
        
        lines = self.getLines(file_name)
        measure = []
        for line in lines:
            measure.append(line.measure)
        return measure
    
    def getNotes(self, file_name): 
        """
        Get note information, return an array of string.
        """
        
        measures = self.getMeasures(file_name)
        notes = []
        note = []
        for measure in measures:
            for line_measure in measure:
                #separate the measures by regular expression, then analyze the duration
                #p = re.compile('((\^|_|=)?[a-gA-G]((,*)|(\'*))?([2-9]?//*[2-9]?)?([2-9])?(>*)?(<*)?)')
                p = re.compile('(((\^|_|=)?[a-gA-G]((,*)|(\'*))?([2-9]?//*[2-9]?)?([2-9])?(>*)?(<*)?)|(#ending))')
                
                #p = re.compile('((\^|_|=)?[a-gA-G]([2-9]?//*[2-9]?)?([2-9])?((<*)?|(>*)?)?)')
                note = p.findall(line_measure.__str__())
                for i in range(len(note)):
                    notes.append(note[i][0])
                note =[]
                #print(re.findall('(\^|_|=)?[a-gA-G]([2-9]?//*|[2-9]?)(((<*)?|(>*)?)?)?', line_measure.__str__()))
        return notes
            
#     #get pitch information
#     #without ABCPArser.
#     #lost the repeat information.
#   
#     def getPitch(self, file_name):
#         #根据调性出现频率，转化调性至C大调(或频率最高的调性)
#         pitch_list = [(0) for i in range(33)]
#          
#          
#         #lines that are after transposition
#         lines = self.keyNormalization(file_name)
#         for line in lines:
#             p = re.compile('((\^|_|=)?[a-gA-G]((,*)|(\'*))?)')
#             note = p.findall(line)
#              
#             for i in range(len(note)):
#                 pitch_list[self.pitch_dictionary[note[i][0].__str__()]] = 1
#                 self.pitch.append(pitch_list)
#                 pitch_list = [(0) for i in range(33)]
#                  
#         return self.pitch

    #723 pieces of data lost
    #fixed the lost problem.
    def getPitch(self,file_name):
        """
        Get pitch information, return an array of 34 dimension array. Refer to pitch.dat.
        """
        
        notes = self.getNotes(file_name)
        pitch_list = [(0) for i in range(33)]
        pitch_timesteps = []
          
        for note in notes:
            #p = re.compile('((\^|_|=)?[a-gA-G]((,*)|(\'*))?)')
            p = re.compile('(((\^|_|=)?[a-gA-G]((,*)|(\'*))?)|(#ending))')
            current_notes = p.findall(note)
                
            for i in range(len(current_notes)):
                if current_notes[i][0].__str__() != '#ending':
                    pitch_list[self.pitch_dictionary[current_notes[i][0].__str__()]] = 1
                    pitch_timesteps.append(pitch_list)
                    pitch_list = [(0) for i in range(33)]
                else:
                    self.pitch.append(pitch_timesteps)
                    pitch_timesteps = []
                       
        return self.pitch 
 
 
    def getDuration(self, file_name):
        """
        Get duration information, return an array of 23 dimension array. Refer to Duration.dat.
        """
       
        notes = self.getNotes(file_name)
        duration_list = [(0) for i in range(23)]
        duration_timesteps = []
        
        new_nextNoteDurationPlus = 0.0
        new_nextNoteDurationFlag = False
        count = 0
        
        for note in notes:
            
            note_analysis = ABCParser.Note()
            if count == 0:
                text, current_duration, nextNoteDurationPlus, nextNoteDurationFlag = note_analysis.parse(note)
                count = count + 1
            else:
                text, current_duration, nextNoteDurationPlus, nextNoteDurationFlag = note_analysis.parse(note, new_nextNoteDurationPlus, new_nextNoteDurationFlag)
            if text == '#ending':
                #self.duration append a vector of the duration information of a note
                self.duration.append(duration_timesteps)
                duration_timesteps = []
            else:
                
                duration_list[self.duration_dictionary[current_duration]] = 1
                duration_timesteps.append(duration_list)
                duration_list = [(0) for i in range(23)]

            new_nextNoteDurationPlus = nextNoteDurationPlus
            new_nextNoteDurationFlag = nextNoteDurationFlag

        return self.duration
    
    
    
    
    