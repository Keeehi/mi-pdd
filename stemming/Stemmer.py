#!/usr/bin/python3
import pexpect


class Stemmer:
    def __init__(self):
        self.p = pexpect.spawn('./stemwords')

    def stem(self, word):
        self.p.sendline(word)
        self.p.expect('\r\n')
        self.p.expect('\r\n')
        return self.p.before.decode('utf-8')