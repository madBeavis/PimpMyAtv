#!/bin/bash
adb disconnect

for i in $(seq 33 75); do
	adb connect 192.168.8.$i;
done

readarray -d ' ' devices < <(adb devices -l | cut -f1 -d' ' | tail -n+2 | xargs);

for device in "${devices[@]}"; do
	echo "updating magisk on "$device;	
	# obtain follwing from https://github.com/Astu04/AtlasScripts/blob/main/magisk_update.sh
	adb -s $device push /home/adbupdater/magisk_update.sh /sdcard;
	adb -s $device shell "su -c 'chmod +x /sdcard/magisk_update.sh && /system/bin/sh /sdcard/magisk_update.sh'";
done

adb disconnect
