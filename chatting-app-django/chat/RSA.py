# -*- coding: utf-8 -*-
import time

a = time.time()
import pyaes

import base64
from numba import njit
from sympy import *


@njit
def numba_pow(a, b, c):
    return pow(a, b, c)


def just_pow(a, b, c):
    return pow(a, b, c)


class Rsa:
    def __init__(self):
        # Простые числа
        self.a = randprime(8000000, 9000000)
        self.b = randprime(7999992, 8000000)
        self.N = self.a * self.b
        self.func_eiler = (self.a - 1) * (self.b - 1)
        i = 2
        while i < self.func_eiler:
            self.open_ecsp = nextprime(i)
            if self.func_eiler % self.open_ecsp != 0:
                break
            i += 1
        j = 1
        while i < self.func_eiler:
            if (self.func_eiler * j + 1) / self.open_ecsp % 1 == 0:
                self.secrit_ecsp = int((self.func_eiler * j + 1) / self.open_ecsp)
                break
            j += 1

    def get_secret_key(self):
        a = [self.N, self.secrit_ecsp]
        wordList = [num.to_bytes(7, byteorder='big') for num in a]
        encoded = b''.join(wordList)
        return base64.b64encode(encoded).decode('ascii')

    def get_open_key(self):
        a = [self.N, self.open_ecsp]
        wordList = [num.to_bytes(7, byteorder='big') for num in a]
        encoded = b''.join(wordList)
        return base64.b64encode(encoded).decode('ascii')

    def encript(self, m, key=None):
        list_word_index = [
            just_pow(ord(i), self.open_ecsp if key is None else
            [int.from_bytes(base64.b64decode(key)[i:i + 7], byteorder='big') for i in
             range(0, len(base64.b64decode(key)), 7)][1], self.N if key is None else
                     [int.from_bytes(base64.b64decode(key)[i:i + 7], byteorder='big') for i in
                      range(0, len(base64.b64decode(key)), 7)][0]) for i in m]
        wordList = [num.to_bytes(7, byteorder='big') for num in list_word_index]
        encoded = b''.join(wordList)
        return base64.b64encode(encoded).decode('ascii')

    def decript(self, enc_m, key=None):
        m = [int.from_bytes(base64.b64decode(enc_m)[i:i + 7], byteorder='big') for i in
             range(0, len(base64.b64decode(enc_m)), 7)]
        f = []
        for i in range(len(m)):
            resalt = just_pow(m[i], self.secrit_ecsp if key is None else
            [int.from_bytes(base64.b64decode(key)[i:i + 7], byteorder='big') for i in
             range(0, len(base64.b64decode(key)), 7)][1], self.N if key is None else
                              [int.from_bytes(base64.b64decode(key)[i:i + 7], byteorder='big') for i in
                               range(0, len(base64.b64decode(key)), 7)][0])
            f.append(resalt)
        final_result = [chr(i) for i in f]
        return ''.join(final_result)


import time

import base64
import random
import string
import pyaes


class Aes:
    def __init__(self, key=None):
        # self.message = message
        self.key = ''.join(random.choice(string.ascii_lowercase) for i in range(32))

    def print_key(self):
        return self.key

    def enc_aes(self, message, key=None):
        plaintext = message.encode('utf-8')
        key = key.encode('utf-8')
        aes = pyaes.AESModeOfOperationCTR(key)
        str_aes = aes.encrypt(plaintext)
        txt = base64.b64encode(str_aes).decode('utf-8')
        return txt

    def dec_aes(self, message, key=None):
        m = base64.b64decode(message)
        aes = pyaes.AESModeOfOperationCTR(key.encode('utf-8'))
        decrypted = aes.decrypt(m)
        return decrypted.decode('utf-8')