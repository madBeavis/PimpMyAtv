#!/bin/bash
adb disconnect
sleep 2s
adb connect 192.168.8.51:5555
sleep 2s
scrcpy -b1M -m512 --window-title Atv01
