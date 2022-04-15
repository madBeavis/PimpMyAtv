rem Windows batch file to use scrcpy on one device
rem -b option sets bandwidth
rem -m option sets resolution
rem --render-driver=opengl works better on my laptop, ymmv

adb disconnect
timeout 2

adb connect 192.168.8.51:5555
timeout 2

rem running setup to monitor
scrcpy -b8m -m1024 --window-title atv001 --render-driver=opengl --max-fps=30
