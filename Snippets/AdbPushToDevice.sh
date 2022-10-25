#!/bin/bash

mapfile -t devices < devicelist.txt

for i in "${devices[@]}"; do
adb connect $i 
adb -s $i shell settings put global http_proxy proxy_ip:proxy_port
adb -s $i shell "su -c am broadcast -a android.intent.action.PROXY_CHANGE"
adb disconnect $i
