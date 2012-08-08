#!/usr/bin/env python

from __future__ import unicode_literals, print_function, nested_scopes

import sys, time, fileinput
from collections import OrderedDict

def word_generator(input_):
    flags = ''
    for line in input_:
        if line.isspace():
            flags = '\n'
        for word in line.split():
            if word.endswith('.'):
                flags += '.'
            yield (word, flags)
            flags = ''

def output_thing(sim_words = 2, columns = 80):

    words = OrderedDict()

    def inner_thing(word):

        if len(words) > sim_words - 1:
            words.popitem(last=False)
        
        next_idx = 0
        if len(words) > 0:
            last_idx, last_word = words.popitem()
            words[last_idx] = last_word # just put it back
            if len(last_word) + len(word) + last_idx + 1 <= columns:
                next_idx = last_idx + len(last_word) + 1

        words[next_idx] = word

        buffer_ = ' ' * columns
        for idx, w in words.iteritems():
            w_len = len(w)
            buffer_ = buffer_[0:idx] + w + buffer_[idx+len(w):]

        return buffer_

    return inner_thing

if __name__ == '__main__':
    output_thing_args = {'columns': 60}
    outputter = output_thing(**output_thing_args)
    import sys, codecs
    # TODO: Read standard input
    for arg in sys.argv[1:]:
        for word, flags in word_generator(codecs.open(arg, 'r', 'utf-8')):
            if '\n' in flags:
                time.sleep(0.5)
                outputter = output_thing(**output_thing_args)
            sys.stdout.write('\r' + outputter(word))
            sys.stdout.flush()
            time.sleep(0.1) # TODO: use a better method for timing
    print()
