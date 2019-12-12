call "C:\Program Files (x86)\Microsoft Visual Studio\2017\BuildTools\Common7\Tools\VsDevCmd.bat" -arch=amd64

cd deps\chmlib\src

set opts=/MD /DWIN32 /DNDEBUG /D_LIB /D_UNICODE /DUNICODE /D_CRT_SECURE_NO_WARNINGS /wd4996

cl /c %opts% chm_lib.c lzx.c
lib /out:chm.lib /nologo chm_lib.obj lzx.obj
