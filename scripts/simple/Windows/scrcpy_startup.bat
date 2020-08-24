adb disconnect
timeout 2
adb connect 192.168.8.51:5555
timeout 2
scrcpy -b2M -m512 --window-title atv01 --render-driver=opengl
