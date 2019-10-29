#!/bin/bash
adb disconnect
sleep 1s
adb connect 192.168.8.51:5555
sleep 1s
scrcpy -b1M -m512 --window-title Atv01
