#!/bin/bash
adb disconnect

for i in $(seq 101 150); do
	adb connect 192.168.8.$i;
done

readarray -d ' ' devices < <(adb devices -l | cut -f1 -d' ' | tail -n+2 | xargs);

for device in "${devices[@]}"; do
	echo "install playstore on "$device;
	# download Google Play Store 36.9.16-21 from apkmirror or equivalent
	adb -s $device install -r playstore.apk;
	echo "enable playstore on "$device;
	adb -s $device shell "pm enable com.android.vending"
done

adb disconnect
