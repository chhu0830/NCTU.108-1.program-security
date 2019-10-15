# NCTU.108-1.program-security


## Lab 0x01 What The Hell [rev]

```
Flag   : FLAG{BABY_REVERSE_123}
Points : 50
```

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
