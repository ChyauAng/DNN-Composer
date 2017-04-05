# The preprocessing part<br>

　[The ABC notation](http://trillian.mit.edu/~jc/music/abc/doc/ABCtut.html), compared with the MIDI, is more human-oriented than machine-oriented. So a preprocessing procedure is necessary. This part aims at extracting useful information from the raw text data of the data set, by processing the prefixes and suffixes of each note.<br>

　The main files in this part and their functions are as follows:<br>
　　ABCParser.py : ABC parser for ABC notation files.<br>
　　DataPreprocess.py : extracting the pitch and duration information from the data set.<br>
　　GlobalConstant.py : several global constants in this part.<br>

　Pitch.dat and Duration.dat are uploaded. The files contain the extracted information mentioned above. They all are normalized to reduce redundancies in representations. The normalization process is in DataPreprocess.py.
