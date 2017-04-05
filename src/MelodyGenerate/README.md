 ## The melody generating part
 
 　This part aims at generating new melodies by the nerual network model. The nerual network consists of two part: the melody model and the rhythm part.<br>
 　The main files in this part and their functions are as follows:<br>
　　GetData.py : get the inputs of the melody model and the rhythm model from the pitch and duration.<br>
　　MelodyGenerater.py : build the models, train and test and evaluate them, then generate new melodies.<br>
　　generaterTester.py : the current entry of the work.<br>
   
 　This part is very memory-consuming. The optimization is now in process.<br>
