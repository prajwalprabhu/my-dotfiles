#! /bin/bash 
picom &
wal -R &
/usr/lib/jvm/java-14-openjdk/bin/java -Xmx1024m -jar /opt/xdman/xdman.jar -m &
dunst &
clipmenud &
nm-applet &
mocp &

