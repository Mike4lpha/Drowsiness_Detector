To autorun a python file in raspberry pi without computer:

cd /home/pi/.config
mkdir autorun
cd autorun
touch autorun.desktop
vim autorun.desktop
#########################################
[Desktop Entry]

Exec=sudo bash /home/pi/on_reboot.sh
#########################################
#close vim editor

cd /home/pi
vim on_reboot.sh
#####################################
#!/bin/bash
source /home/pi/env/bin/activate
cd /home/pi/env/Drowsiness_Detector
python drowsiness.py
######################################
#close vim editor
