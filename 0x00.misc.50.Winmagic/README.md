# Winmagic
Try to debug this program.

Winmagic.cpp
Winmagic.exe
Winmagic.pdb

## PoC
`FLAG{WinDbg_is_very_important_in_windows_security}`
* IDA Pro
  * Find `get_flag` function, then find xor value (`[rsp+0C8h+var_A0]`)
