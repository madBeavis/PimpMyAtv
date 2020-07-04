REM hacky script to fix pd
REM have this batch file and zzz_tim_magisk.sh in the same directory to run
REM make your own list of ip, i used excel


adb disconnect
timeout 10

adb connect 192.168.8.133:5555
adb connect 192.168.8.134:5555

@echo off

SETLOCAL ENABLEDELAYEDEXPANSION 
:: INSTALL ON ALL ATTACHED DEVICES ::
FOR /F "tokens=1,2 skip=1" %%A IN ('adb devices') DO (
    SET IS_DEV=%%B
	if "!IS_DEV!" == "device" (
	    SET SERIAL=%%A
	    echo "adb -s !SERIAL! fix pd pt1 - push file"
	    call adb -s !SERIAL! push zzz_tim_magisk.sh /sdcard/
		echo "adb -s !SERIAL! fix pd pt2 - copy file"
	    call adb -s !SERIAL! shell "su -c 'cp /sdcard/zzz_tim_magisk.sh /data/adb/service.d/'"
		echo "adb -s !SERIAL! fix pd pt3 - chmod file"
	    call adb -s !SERIAL! shell "su -c 'chmod +x /data/adb/service.d/zzz_tim_magisk.sh'"
		echo "remember to reboot after!"
	)
)
ENDLOCAL

:EOF

adb disconnect
timeout 1