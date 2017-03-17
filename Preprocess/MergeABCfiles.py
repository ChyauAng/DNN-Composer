from Preprocess import DataPreprocess

class MergeFiles:
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
        
    def main(self):
        data = []          
        test = DataPreprocess.ABCPreprocess(self.dir_path, self.data)
        test.processFolder()
        
