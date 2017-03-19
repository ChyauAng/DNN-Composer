# DNN-Composer
An experimental work in Python mainly using GNN and CNN for Algorithmic composition.<br>

　This work is inspired by [this paper](https://arxiv.org/abs/1606.07251) and [this paper](https://arxiv.org/abs/1508.06576).<br>
　The main idea of this work is to generate a melody by using GNN and to change its style by using CNN.<br>
　Take the differences between a melody and an image into consideration,the idea metioned above is just a tentative version.<br>
　This work is now under experiment.The final version will be commited once finished.<br>

## The preprocessing part<br>

　[The ABC notation](http://trillian.mit.edu/~jc/music/abc/doc/ABCtut.html), compared with the MIDI, is more human-oriented than machine-oriented. So a preprocessing procedure is necessary. This part aims at extracting useful information from the raw text data of the data set, by processing the prefixes and suffixes of each note.<br>

　The main files in this part and their functions are as follows:<br>
　　ABCParser.py : ABC parser for ABC notation files.<br>
　　DataPreprocess.py : extracting the pitch and duration information from the data set.<br>
　　GetPitchDurationData.py : getting the pitch and duration information and write them in files.<br>
　　GlobalConstant.py : several global constants in this part.<br>

　Pitch.dat and Duration.dat are uploaded. The files contain the extracted information mentioned above. They all are normalized to reduce redundancies in representations. The normalization process is in DataPreprocess.py.
