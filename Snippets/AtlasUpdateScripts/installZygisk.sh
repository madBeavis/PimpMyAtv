#!/bin/bash
adb disconnect

for i in $(seq 101 199); do
	adb connect 192.168.8.$i;
done

for j in $(seq 210 230); do
	adb connect 192.168.8.$j;
done

for k in $(seq 33 75); do
	adb connect 192.168.8.$k;
done

readarray -d ' ' devices < <(adb devices -l | cut -f1 -d' ' | tail -n+2 | xargs);

for device in "${devices[@]}"; do
	echo "installing safetynet fix "$device;	
	adb -s $device push zygisk.zip /sdcard;
	adb -s $device shell "su -c 'magisk --install-module /sdcard/zygisk.zip'";
done

adb disconnect
