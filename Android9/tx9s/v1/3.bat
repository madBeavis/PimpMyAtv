adb shell settings put global http_proxy 192.168.8.20:9100
adb shell settings put global global_http_proxy_host 192.168.8.20
adb shell settings put global global_http_proxy_port 9100
adb shell settings put global package_verifier_user_consent -1
rem adb reboot
rem adb disconnect
