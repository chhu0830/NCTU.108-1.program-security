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
