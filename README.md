this is just a private archive, no docs here.

few notes:
+ `python convert.py src ref dst`
+ xx 3ds ver. save size is `4726152 bytes`, xx ns ver. save size is `4726188 bytes`, the switch ver. has a larger header
+ gu save size is `5159100 bytes`, which has larger dlc storage (for multilanguage) and chat shortcut storage(idk why, but while jp versions use `60` bytes, gu has `44` extra bytes per sentence)
file stucture:
```
# xx 3ds ver.

file+0x00000000
                blah_blah_blah
    +0x00000004
                slots info (0x00000000 - no slots used, 0x01000000 - slot #1 used, others not tested, NEVER edit it if only converting save version)
    +0x00000008
                blah_blah_blah
    +0x0000012A
                dlc cat info #1
    +0x0000026E
                dlc cat info #2 - #50
    +0x00004072
                dlc contents(item packs, event quests etc.) padding might be included
    +0x00126474
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
    +0x0000014E
                dlc cat info #1
    +0x00000292
                dlc cat info #2 - #50
    +0x00004096
                dlc contents(item packs, event quests etc.) padding might be included
    +0x00126498
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
    +0x0000014E
                dlc cat info #1
    +0x00000292
                dlc cat info #2 - #50
    +0x00004096
                dlc contents(item packs, event quests etc.) padding might be included
    +0x0018CC9C
                save slot #1
    +0x002A9D25
                chat shortcuts #1
    +0x002AC55D
                solt #2 - #3
    +0x004EB6E5
                padding?
    +0x004EB8BC
```