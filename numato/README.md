do note that i am not a python programmer, just c# and delphi.

v2, the beta version of power control code for numato relay board, is called 'numato.py'.  see the pdf for features and usages of v2.  the main difference between v2 and v1 is that v1 was only setup for NO relay connections, with v2 a power on command will account the NC/NO setup properly.

it does work with GhostTalker's [RebootMadDevices](https://github.com/GhostTalker/RebootMadDevice).  One thing you must do is to chmod +x RebootMadDevice.py and numato.py files, otherwise you will get permission errors.
