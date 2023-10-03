adb shell settings put global policy_control 'immersive.navigation=*'
adb shell settings put global policy_control 'immersive.null=*'
adb shell settings put secure immersive_mode_confirmations confirmed
adb shell settings put global heads_up_enabled 0
adb shell settings put global bluetooth_disabled_profiles 1
adb shell settings put global bluetooth_on 0
adb shell settings put global package_verifier_user_consent -1

adb push playintegrityfix.zip /sdcard
adb push atlas_config.json /data/local/tmp

adb shell settings put global bluetooth_disabled_profiles 1
adb shell settings put global bluetooth_on 0
adb shell settings put global package_verifier_user_consent 0

adb install magisk263.apk
adb install atlas.apk
adb install power-menu.apk
adb install integritychecker.apk
adb install pogo283-1.apk

adb shell am start com.topjohnwu.magisk/.ui.MainActivity
adb shell sleep 15
adb shell input tap 1850 540
adb shell sleep 15
adb reboot
