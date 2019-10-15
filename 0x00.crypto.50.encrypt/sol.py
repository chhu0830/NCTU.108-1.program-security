#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random


def op1(p, s):
    return sum([i * j for i, j in zip(s, p)]) % 256

def op2(m, k):
    return bytes([i ^ j for i, j in zip(m, k)])

def op3(m, p):
    return bytes([m[p.index(i)] for i in range(len(m))])

def op4(m, s):
    return bytes([s.index(x) for x in m])

def stage0(m):
    random.seed('oalieno')
    p = [int(random.random() * 256) for i in range(16)]
    s = [int(random.random() * 256) for i in range(16)]
    c = b''
    for x in m:
        k = op1(p, s)
        c += bytes([x ^ k])
        s = s[1:] + [k]
    return c

def stage1(m):
    random.seed('oalieno')
    k = [int(random.random() * 256) for i in range(16)]
    p = [i for i in range(16)]
    random.shuffle(p)
    s = [i for i in range(256)]
    random.shuffle(s)

    c = m
    for i in range(16):
        c = op4(c, s)
        c = op3(c, p)
        c = op2(c, k)
    return c

def decrypt(m, key):
    stage = [stage1, stage0]
    for i in map(int, f'{key:08b}'):
        m = stage[i](m)
    return m

c = open('cipher-44be20acf18f8b337ec1792d10b4a471', 'rb').read()

for i in range(256):
    m = c
    p = decrypt(m, i)
    if b'FLAG' in p:
        print(p)
        
