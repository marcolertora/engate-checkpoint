#!/bin/sh

export USER=root
export HOME=/root

exec > /var/log/checkpoint-console.log 2>&1

#xrandr -s 1680x1050
xsetroot -solid gray
setterm -blank 0 -powersave off -powerdown 0
xset -dpms
xset s off
#unclutter -grab &
( cd /opt/checkpoint && python -u console.py ) &
icewm
