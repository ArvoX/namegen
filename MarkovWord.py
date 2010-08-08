#!/usr/bin/python
import random

class Markov:
    def __init__(self, file, size):
        self.size = size
        self.starts = []
        self.cache = {}
        self.file_to_words(file)
        self.parse_words()

    def file_to_words(self, file):
        file.seek(0)
        data = file.read()
        self.words = data.split("\n")

    def tuples(self, word):
        if len(word) < self.size - 1:
            return

        word = word + "\n"

        for i in range(len(word) - self.size):
            yield (word[i:i+self.size], word[i+self.size])


    def parse_words(self):
        for word in self.words:
            self.starts.append(word[:self.size])
            for key, next in self.tuples(word):
                if key in self.cache:
                    self.cache[key].append(next)
                else:
                    self.cache[key] = [next]

    def generate_word(self):
        key = random.choice(self.starts)
        word = key
        next = random.choice(self.cache[key])
        while next != "\n":
            word = word + next
            key = key[1:] + next
            next = random.choice(self.cache[key])
        return word

from optparse import OptionParser

def main():
    parser = OptionParser()
    parser.add_option('-p', type='int', dest='prev_num', default=3,
                      help='number of previous letters to base chain on')
    parser.add_option('-n', type='int', dest='num', default=5,
                      help='number of generated words')
    parser.add_option('-s', '--source-text', type='string',
                      default='wordlist-en.txt', dest='source',
                      help='file to use as basis for generating the words')
    (options, args) = parser.parse_args(['-p','3','-n','10','-s','names.txt'])

    file = open(options.source)
    markov = Markov(file, options.prev_num)
    for i in range(options.num):
        print markov.generate_word().capitalize()

if __name__ == '__main__':
    print 'Content-Type: text/plain\n'
    main()
