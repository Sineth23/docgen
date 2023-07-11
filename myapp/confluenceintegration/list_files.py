import os

def list_files(directory):
    # Specify the directory path
    directory = f"/home/ec2-user/myproject/{directory}/.autodoc/docs/markdown"
    
    # Get the list of files in the directory
    files = os.listdir(directory)
 
    return files
