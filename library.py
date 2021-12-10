import os
import json
from pathlib import Path
import subprocess

import eyed3

from storage import GoogleStorage

class Library():

    fields_of_interest = {'artist', 'title'}

    def __init__(self, folder):

        self.folder = Path(folder)
        self.name = self.folder.name
        self.tracks = {}

        self.temp_path = Path('data/temp')
        self.temp_path.mkdir(parents=True, exist_ok=True)

        #TODO check for json lib first, then check files, then check remote
        if (self.folder / 'library.json').exists():
            self.load_library_file()
        else:
            self.import_folder()
        
    def load_library_file(self):
        with (self.folder / 'library.json').open() as f:
            self.tracks = json.load(f)

    def import_folder(self):

        assert not self.tracks

        for file_ in self.folder.iterdir():
            filename = str(file_.relative_to(self.folder))
            print(filename)

            metadata = eyed3.load(file_)
            if not metadata:
                continue

            data = {}
            for tag in self.fields_of_interest:
                data[tag] = getattr(metadata.tag, tag)

            self.tracks[filename] = data

        with (self.folder / 'library.json').open('w') as f:
            json.dump(self.tracks, f)
            
    def get_list(self):

        return(self.tracks)

    def get(self, name):

        if name not in self.tracks:
            raise Exception

        input_file = self.folder / name
        output_file = str(self.temp_path / (name + '.wav'))
        subprocess.run(['ffmpeg', '-y', '-i', input_file, '-vn', '-acodec', 'pcm_s16le', '-ac', '2', '-ar', '44100', '-f', 'wav', output_file])

        return (output_file)


class RemoteLibrary(Library):

    def __init__(self, bucket, name, token):

        self.bucket = bucket

        folder = Path('data') / name
        folder.mkdir(parents=True, exist_ok=True)

        self.storage = GoogleStorage()
        self.storage.initialize(bucket, token)

        self.storage.get(f'{name}/library.json', folder / 'library.json')

        super().__init__(folder)

    def get(self, name):

        input_file = self.folder.name + '/' + name

        self.storage.get(input_file, self.folder / name)

        return super().get(name)

