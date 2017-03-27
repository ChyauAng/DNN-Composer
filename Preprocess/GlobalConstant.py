#global declaration
global index0
global index1
global index2
global index3
global index4
global index5
global index6
global index7
global index8
global index9
global index10
global index11
global index12
global index13
global index14
global index15
global index16
global index17
global index18
global index19
global index20
global index21
global index22

global nextNoteDurationBase

global note

global pitch_train
global pitch_test

global duration_train
global duration_test

#used for getting duration information
index0 = 1/4
index1 = 1/3
index2 = 1/2
index3 = 3/4
index4 = 3/8
index5 = 5/8
index6 = 2/3
index7 = 2/5
index8 = 4/9
index9 = 4/5
index10 = 1.0 
index11 = 3/2
index12 = 4/3
index13 = 9/8
index14 = 2.0
index15 = 8/3
index16 = 9/4
index17 = 7/2
index18 = 3.0
index19 = 4.0
index20 = 9/2
index21 = 6.0
index22 = 8.0

#used for gettiing pitch information
note = ['G,', '^G,', '_G,', '=G,',
        'A,', '^A,', '_A,', '=A,',
        'B,', '^B,', '_B,', '=B,',
        'C', '^C', '_C', '=C',
        'D', '^D', '_D', '=D',
        'E', '^E', '_E', '=E',
        'F', '^F', '_F', '=F',
        'G', '^G', '_G', '=G',
        'A', '^A', '_A', '=A',
        'B', '^B', '_B', '=B',
        'c', '^c', '_c', '=c',
        'd', '^d', '_d', '=d',
        'e', '^e', '_e', '=e',
        'f', '^f', '_f', '=f',
        'g', '^g', '_g', '=g',
        'a', '^a', '_a', '=a',
        'b', '^b', '_b', '=b',
        'c\'', '^c\'', '_c\'', '=c\'',
        'd\'', '^d\'', '_d\'', '=d\'',
        '%ending']        


#nextNoteDurationBase is the base value of duration

nextNoteDurationBase = 1.0

pitch_train = []
pitch_test = []

duration_train = []
duration_test = []




