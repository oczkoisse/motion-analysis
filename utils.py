# Class to interact (read, write) playlist files
class Playlist():
    # Initialize the paths to files to be written to the playlist file
    def __init__(self, files):
        self.files = files

    def write(self, file_name):
        # Creating a playlist file
        pls_file = open(file_name, 'w')

        # Header of the .pls format
        pls_file.write('[playlist]\n\n')
    
        for i in range(len(self.files)):
            pls_file.write('File' + str(i+1) + '=' + files[i] + '\n\n')
    
        # The footer for .pls format
        pls_file.write('NumberOfEntries=' + str(len(files)) + '\n')
        pls_file.write('Version=2')
        pls_file.close()

    def read(self, file):
        pass
