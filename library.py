import os
from pathlib import Path
import subprocess


class Library():

    def __init__(self):

        self.tracks = []

        self.folder = Path(os.getenv('RD_LIBRARY'))

        self.temp_path = Path('data/temp')
        self.temp_path.mkdir(parents=True, exist_ok=True)
        
        self.import_folder()

    def import_folder(self):

        if not self.folder:
            return

        for file_ in self.folder.iterdir():
            self.tracks.append(str(file_.relative_to(self.folder)))
            
    def get_list(self):

        return([[f, '.'] for f in self.tracks])

    def get_name(self, index):
        input_file = self.tracks[index]
        return input_file

    def get(self, name):
        input_file = self.folder / name
        output_file = str(self.temp_path / (name + '.wav'))
        subprocess.run(['ffmpeg', '-y', '-i', input_file, '-vn', '-acodec', 'pcm_s16le', '-ac', '2', '-ar', '44100', '-f', 'wav', output_file])

        return (output_file)

