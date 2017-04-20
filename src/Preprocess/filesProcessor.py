from Preprocess import dataPreprocess

class FilesProcess:
    """
    Gather all ABC files to dataset.dat
        
    Properties
    ----------
    dir_path
        The path of the directory.
    data
        The ABC files information.
    """
    
    
    def __init__(self, dir_path, data = []):
        self.dir_path = dir_path
        self.data = data
        
    def main(self, file_name):
        data = []          
        test = dataPreprocess.ABCPreprocess(self.dir_path, self.data)
        test.processFolder(file_name)
        
    def plusEnding(self, file_name):
        """
        Preprocess the 24th dimension of pitch and duration.
        """
        with open(file_name, 'r') as f:
            lines = f.readlines()
            data = []
            i = 0
            for line in lines:
                if line[0 : 2] == 'X:' and i != 0:
                    data += '|#ending|\n'
                data += line
                i = i + 1
            data += '|%ending|\n'
                
        file_object = open(file_name, 'w')
        file_object.writelines(data)
        file_object.close()
        
