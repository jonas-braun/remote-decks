import os
from pathlib import Path
import subprocess


class Library():

    def __init__(self):

        self.tracks = []
        
        self.import_folder()

    def import_folder(self):

        folder = os.getenv('RD_LIBRARY')

        if not folder:
            return

        for file_ in Path(folder).iterdir():
            self.tracks.append(str(file_))
            


    def get_list(self):

        return([[f, '.'] for f in self.tracks])

    def get(self, index):
        input_file = self.tracks[index]
        output_file = str(Path('data/temp') / (Path(input_file).name + '.wav'))
        subprocess.run(['ffmpeg', '-y', '-i', input_file, '-vn', '-acodec', 'pcm_s16le', '-ac', '2', '-ar', '44100', '-f', 'wav', output_file])

        return (output_file)
