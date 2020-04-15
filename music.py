import os
import random


class Song:
    def __init__(self, path, category=None):
        self.path = path
        self.name = os.path.split(self.path)[-1].split(".")[0]
        self.category = category

    def get_song(self):
        with open(self.path, 'r') as f:
            return "\n".join(f.readlines())


class Music:
    def __init__(self, song_dir="songs"):
        self.dir = song_dir
        self.songs = []
        self.categories = []

        for dir in os.listdir(self.dir):
            self.categories.append(dir)
        for root, dirs, files in os.walk(self.dir):
            path = root.split(os.sep)
            for file in files:
                self.songs.append(Song(root + os.sep + file, path[-1]))

    def random(self, cat=None):
        song = random.choice(self.songs)
        if cat in self.categories:
            while song.category != cat:
                song = random.choice(self.songs)
        return song

    def play(self, name):
        # print(f"Looking for song {name}")
        for song in self.songs:
            if name.lower() in song.name.lower():
                return song.get_song()


def main():
    m = Music()
    for song in m.songs:
        print(song.name)


if __name__ == '__main__':
    main()
