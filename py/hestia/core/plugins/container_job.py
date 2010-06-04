class Job:
    """this is a container for jobs"""
    
    def __init__(self,id,label):
        """
          instance variables:
          id: a unique job id
          label: a label (url to fect, file to read, whatever)
          result: this will store the result (content of the file, whatever)
        """
        self.id=id
        self.label=label
        self.result=None
