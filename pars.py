import mido
import os


def find(exc, directory):
    list_files = []
    for files in os.walk(directory):
        for file in files[2]:
            if os.path.splitext(file)[1] in exc:
                list_files.append(file)
    return list_files


class TextParser:

    def __init__(self, file):
        if file:
            self.file = mido.MidiFile(file)
            self.charset = self.file.charset

    def parse(self):
        text_music = ""
        time = 0
        tempo = 500000
        text_music_by_time = []
        for message in self.file.tracks[0]:
            if message.type == 'set_tempo':
                tempo = message.tempo
        for message in self.file.tracks[2]:
            if message.type == "text":
                words = message.text.encode(self.charset).decode('cp1251')
                if '@' in words:
                    continue
                if '\\' in words:
                    words = '\n' + words.replace('\\', '\n')
                if '/' in words:
                    words = '\n' + words.replace('/', '')
                time += message.time
                time_in_seconds = mido.tick2second(time,
                                                   self.file.ticks_per_beat,
                                                   tempo)
                text_music_by_time.append((words, time_in_seconds))
                text_music += words
        return text_music_by_time

    def change_tempo(self, filename, tempo):
        if os.path.isfile(filename):
            return
        new_mid = mido.MidiFile()
        new_mid.ticks_per_beat = self.file.ticks_per_beat
        for track in self.file.tracks:
            new_track = mido.MidiTrack()
            new_mid.tracks.append(new_track)
            for msg in track:
                if msg.type == 'set_tempo':
                    if msg.tempo // tempo > 16777215:
                        msg.tempo = 16777215
                    else:
                        msg.tempo = msg.tempo // tempo #меньше - быстрее
                new_track.append(msg)
        self.file = new_mid
        new_mid.save('{}'.format(filename))

    def parse_only_text(self, text):
        words = ""
        for word in text:
            words += word[0]
        return words

    def get_full_time(self):
        minutes, seconds = divmod(self.file.length, 60)
        minutes = round(minutes)
        seconds = round(seconds)
        time_format_all = '{:02d}:{:02d}'.format(minutes, seconds)
        return time_format_all
