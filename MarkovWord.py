#!/usr/bin/python
import random
import os

class Markov:
    def __init__(self):
        self.size = 3 
        self.starts = []
        self.cache = {}
        if(os.path.getmtime('names.txt') > os.path.getmtime('cache.file')):
	    file = open('names.txt')
	    self.file_to_words(file)
            self.parse_words()
	    cachefile = open('cache.file', 'w')
	    cachefile.write(repr(self.cache))
	    cachefile.close()
	    self.file.close()
	else:
	    cachefile = open('cache.file')
	    self.cache = eval(cachefile.read())
	    cachefile.close()
	    self.starts = self.cache.keys()

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

def main():
    markov = Markov()
    for i in range(10):
        print markov.generate_word().capitalize()

if __name__ == '__main__':
    print 'Content-Type: text/plain\n'
    main()
