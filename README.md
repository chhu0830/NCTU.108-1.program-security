# NCTU.108-1.program-security

## [Lab 0x01] What The Hell
`rev, 50 pts` `FLAG{BABY_REVERSE_123}`

> 跟地獄世界打招呼，摸摸找找 Flag 在哪。
> 
> [hellWorld.exe](https://edu-ctf.csie.org/files/hellWorld-42c3475ca77178982fac30821bbb480e.exe)  
> [whatTheHell.exe](https://edu-ctf.csie.org/files/whatTheHell-6eb0d34031d2621537169368490a28e0.exe)

1. IDA

   ```
   if ( argc != 1 && !strcmp(argv[1], "/get_flag") )
   ...
   ```

2. `$ whatTheHell.exe /get_flag`


## [0x01] Back to the Future
`rev, 50 pts` `FLAG{PE_!S_EASY}`

> 一九八五年科學家聖豪成功在實驗室研製了軟體時光機，並將開發時光機的「核心機密」埋藏在時光機軟體中。
>
> 而時光機的機密因為保存技術而有半衰期會逐年衰變，逐漸變為看不懂的資訊，而時光機本身配有 Time Machine Guard 用來抵抗外來研究員嘗試分析破解時光機。
> 
> 請嘗試在不觸發 Time Machine Guard 的情況下回到過去盜取製造時光機的機密吧！！！
> 
> [KeyChecker.exe](https://edu-ctf.csie.org/files/KeyChecker-97d70caa80f4ab9e039f0d8899a5e4bb.exe)

1. 前面有複雜的運算跟條件，但其實最後 `Buffer` 就是 `byte_408008`，
   然後最後 `Buffer ^= byte_40801c`。
2. 因為 `byte_408008` 跟 `byte_40801c` 都已知，直接 xor 就有 flag。


## [0x02] IDAmudamudamuda
`rev, 100 pts` `FLAG{y3s!!y3s!!y3s!!0h_my_g0d!!}`

> ShengHao’s HW1 was too kind, try this.
> 
> [IDAmudamudamuda.exe](https://edu-ctf.csie.org/files/IDAmudamudamuda-22a715976170be268162628bda2df09d.exe)

This program take two value as input.
One is `seed` and another is `flag`.
Use `<S-F12>` and `cross reference` in IDA to find main function.
There are two important functions related to the input,
which are `sub_5D1070(v1)` and `sub_5D1270(&v2)`.
`v1` is the `seed`, and `v2` is the `flag`.

### sub\_5D1070(char a1)
This function take `seed` as parameter.
Most of the code are complicated,
but only a small part of the function is related to the paramter.

```c
...
for ( l = j + 33; l < *(_DWORD *)(i + 8); ++l )
{
  if ( *(_BYTE *)(l + v8) == 69 )
  {
    for ( m = 0; ; ++m )
    {
      result = l + v8;
      if ( !*(_BYTE *)(l + v8 + m) )
        break;
      *(_BYTE *)(l + v8 + m) += a1;
    }
    return result;
  }
  result = l + 1;
}
...
```

Accoring to the rest of the code, `v8` is an address.
The code shows that it will find `69` from `l + v8` and start adding `seed` to each of the bytes until reaching `0`.
We can find the original data by the debugger.

```
\x45\x7b\xdc\x41\xb7\x35\xec\xf0\xf0\xf0\xf0\xdb\xf9\x7b\x35\xec\x73\xb0\xf1\x79\x35\xec\x7b\x3d\xfc\xf3\x3d\xec\xff\xae\x01\x75\xc2\x64\x15\x7b\x35\xf8\xf3\x35\xec\xff\xae\xf8\x73\xb1\x13\x73\xe1\x56\xff\xae\xc1\x7b\x35\xfc\xf3\x35\xec\xff\xae\xf8\x2b\xc1\x64\xf4\x23\xb0\xdb\xf7\xdb\xb5\xa8\xf1\xf0\xf0\xf0\x7b\xd5\x4d\xb3
```

### sub\_5D1270(const char \*a1)
This function will copy some data to `v2` and execute it as a function.
The data is the `data` mentioned in `sub_5D1070(char a1)`.

```c
...
if ( strlen(a1) == 32 )
{
  v2 = VirtualAlloc(0, 0xC8u, 0x1000u, 0x40u);
  qmemcpy(v2, &unk_5D4058, 0xC8u);
  result = ((int (__cdecl *)(const char *, void *))v2)(a1, &unk_5D4018);
}
...
```

The first command of a function usually is `push ebp`, which is `0x55`,
and the first byte of the `data` is `0x45`.
Thus, the seed should be `16`, and we can get the function instructions.

```
 0:   55                      push   ebp
 1:   8b ec                   mov    ebp,esp
 3:   51                      push   ecx
 4:   c7 45 fc 00 00 00 00    mov    DWORD PTR [ebp-0x4],0x0
 b:   eb 09                   jmp    0x16
 d:   8b 45 fc                mov    eax,DWORD PTR [ebp-0x4]
10:   83 c0 01                add    eax,0x1
13:   89 45 fc                mov    DWORD PTR [ebp-0x4],eax
16:   8b 4d 0c                mov    ecx,DWORD PTR [ebp+0xc]
19:   03 4d fc                add    ecx,DWORD PTR [ebp-0x4]
1c:   0f be 11                movsx  edx,BYTE PTR [ecx]
1f:   85 d2                   test   edx,edx
21:   74 25                   je     0x48
23:   8b 45 08                mov    eax,DWORD PTR [ebp+0x8]
26:   03 45 fc                add    eax,DWORD PTR [ebp-0x4]
29:   0f be 08                movsx  ecx,BYTE PTR [eax]
2c:   83 c1 23                add    ecx,0x23
2f:   83 f1 66                xor    ecx,0x66
32:   0f be d1                movsx  edx,cl
35:   8b 45 0c                mov    eax,DWORD PTR [ebp+0xc]
38:   03 45 fc                add    eax,DWORD PTR [ebp-0x4]
3b:   0f be 08                movsx  ecx,BYTE PTR [eax]
3e:   3b d1                   cmp    edx,ecx
40:   74 04                   je     0x46
42:   33 c0                   xor    eax,eax
44:   eb 07                   jmp    0x4d
46:   eb c5                   jmp    0xd
48:   b8 01 00 00 00          mov    eax,0x1
4d:   8b e5                   mov    esp,ebp
4f:   5d                      pop    ebp
50:   c3                      ret
```

We know `unk_5D4018`, and we can just reverse the calculation and get the flag.
