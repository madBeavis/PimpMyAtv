#!/bin/bash
adb disconnect
for i in $(seq 72 73); do
	adb connect 192.168.8.$i;
done

readarray -d ' ' devices < <(adb devices -l | cut -f1 -d' ' | tail -n+2 | xargs);

for device in "${devices[@]}"; do
	echo "removing mad boot files for "$device;
	adb -s $device shell "su -c 'mount -o remount,rw /system && rm /etc/init.d/42mad && rm /etc/init.d/01madbootstrap'";
	adb -s $device reboot;
done

adb disconnect
