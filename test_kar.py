import os
import pars
import unittest


class TestParser(unittest.TestCase):
    directory = os.getcwd()
    directory_image = os.path.join(directory, 'backgrounds')
    file = os.path.join(directory, 'Серебро.kar')

    def test_music_length(self):
        text = pars.TextParser(self.file)
        self.assertEqual(text.get_full_time(), '04:29')

    def test_parser_only_text(self):
        text = pars.TextParser(self.file)
        words = text.parse()
        text_song = text.parse_only_text(words).split()
        self.assertEqual(len(text_song), 101)

    def test_parse_with_time(self):
        text = pars.TextParser(self.file)
        words = text.parse()
        self.assertEqual(len(words), 186)

    def test_parse_time(self):
        text = pars.TextParser(self.file)
        words = text.parse()
        for i in words:
            if i[1] == 'не':
                self.assertEqual(int(i[2]), 7)
                return

    def test_right_encoding(self):
        text = pars.TextParser(self.file)
        self.assertEqual(text.charset, 'latin1')

    def test_finder_picture(self):
        directory = os.getcwd()
        directory_image = os.path.join(directory, 'backgrounds')
        finder = pars.Finder(directory_image, directory)
        self.assertEqual(len(finder.find_picture()), 6)

    def test_finder_music(self):
        directory = os.getcwd()
        directory_image = os.path.join(directory, 'backgrounds')
        finder = pars.Finder(directory_image, directory)
        self.assertEqual(len(finder.find_music()), 2)


if __name__ == '__main__':
    if __name__ == '__main__':
        unittest.main()
