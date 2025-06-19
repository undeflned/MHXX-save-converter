A simple script that converts your MHXX save file to its 3DS or NS jp/global ver,  made for my convenience.

+ Usage: `python convert.py src ref dst`.
+ ALWAYS backup your save files before tampering them.
+ I didn't try the 3DS ver, it should work, but no guarentee.
+ The 3 save files are blank files with corresponding DLCs, the XX switch ver blank save contains most of the DLC otomos.
+ `otomo/` contains a full list of DLC otomos in JP ver.

### Save file stucture:
+ XX 3ds ver. save size is `4726152 bytes`, XX ns ver. save size is `4726188 bytes`, the switch ver. has a larger header
+ GU save size is `5159100 bytes`, which has a larger dlc storage (for multilanguage) and a larger chat shortcut storage(while jp versions use `60` bytes, GU uses `44` extra bytes per sentence)
```
# xx 3ds ver.

file+0x00000000
                blah_blah_blah
    +0x00000004
                slots info (0x00000000 - no slots used, 0x01000000 - slot #1 used, others not tested, NEVER edit it if only converting save version)
    +0x00000008
                blah_blah_blah
    +0x0000002A
                dlc cat info #1
    +0x0000016E
                dlc cat info #2 - #50
    +0x00003F72
                other dlc (item packs, event quests etc.) padding might be included
    +0x00126471
                save slot #1
    +0x002434FD
                chat shortcuts #1
    +0x00244C31
                solt #2 - #3
    +0x00481BB1
                padding?
    +0x00481D88
```
```
# xx switch ver.

file+0x00000000
                blah_blah_blah
    +0x00000028
                slots info (0x00000000 - no slots used, 0x01000000 - slot #1 used, others not tested, NEVER edit it if only converting save version)
    +0x0000002C
                blah_blah_blah
    +0x0000004E
                dlc cat info #1
    +0x00000192
                dlc cat info #2 - #50
    +0x00003F96
                other dlc (item packs, event quests etc.) padding might be included
    +0x00126495
                save slot #1
    +0x00243521
                chat shortcuts #1
    +0x00244C55
                solt #2 - #3
    +0x00481BD5
                padding?
    +0x00481DAC
```
```
# gu

file+0x00000000
                blah_blah_blah
    +0x00000028
                slots info (0x00000000 - no slots used, 0x01000000 - slot #1 used, others not tested, NEVER edit it if only converting save version)
    +0x0000002C
                blah_blah_blah
    +0x0000004E
                dlc cat info #1
    +0x00000192
                dlc cat info #2 - #50
    +0x00003F96
                other dlc (item packs, event quests etc.) padding might be included
    +0x0018CC99
                save slot #1
    +0x002A9D25
                chat shortcuts #1
    +0x002AC55D
                solt #2 - #3
    +0x004EB6E5
                padding?
    +0x004EB8BC
```
