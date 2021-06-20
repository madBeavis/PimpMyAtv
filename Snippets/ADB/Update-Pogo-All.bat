REM windows batch script to install pogo apks to multiple devices
REM make a list of devices in excel or however you want
REM stolen from gosh knows where and from gosh knows who, but credit to our intrepid unknown batch file artist

adb disconnect
timeout 10

adb connect 192.168.8.101:5555
adb connect 192.168.8.102:5555
adb connect 192.168.8.103:5555
adb connect 192.168.8.104:5555
adb connect 192.168.8.105:5555
adb connect 192.168.8.106:5555
adb connect 192.168.8.107:5555
adb connect 192.168.8.108:5555
adb connect 192.168.8.109:5555
adb connect 192.168.8.110:5555
adb connect 192.168.8.111:5555
adb connect 192.168.8.112:5555
adb connect 192.168.8.113:5555
adb connect 192.168.8.114:5555
adb connect 192.168.8.115:5555
adb connect 192.168.8.116:5555
adb connect 192.168.8.117:5555
adb connect 192.168.8.118:5555
adb connect 192.168.8.119:5555
adb connect 192.168.8.120:5555
adb connect 192.168.8.121:5555
adb connect 192.168.8.122:5555
adb connect 192.168.8.123:5555
adb connect 192.168.8.124:5555
adb connect 192.168.8.125:5555
adb connect 192.168.8.126:5555
adb connect 192.168.8.127:5555
adb connect 192.168.8.128:5555
adb connect 192.168.8.129:5555
adb connect 192.168.8.130:5555
adb connect 192.168.8.131:5555
adb connect 192.168.8.132:5555
adb connect 192.168.8.150:5555
adb connect 192.168.8.151:5555
adb connect 192.168.8.152:5555
adb connect 192.168.8.153:5555
adb connect 192.168.8.154:5555
adb connect 192.168.8.155:5555
adb connect 192.168.8.156:5555
adb connect 192.168.8.157:5555

@echo off

SETLOCAL ENABLEDELAYEDEXPANSION 
:: INSTALL ON ALL ATTACHED DEVICES ::
FOR /F "tokens=1,2 skip=1" %%A IN ('adb devices') DO (
    SET IS_DEV=%%B
	if "!IS_DEV!" == "device" (
	    SET SERIAL=%%A
	    echo "adb -s !SERIAL! install-multiple -r base.apk split_config.armeabi_v7a.apk split_config.xxxhdpi.apk"
	    call adb -s !SERIAL! install-multiple -r base.apk split_config.armeabi_v7a.apk split_config.xxxhdpi.apk
		timeout 2
	)
)
ENDLOCAL

:EOF

adb disconnect
timeout 1
