#! /bin/bash
# If the process doesn't exists, start one in background
run() {
	if ! pgrep $1 ; then
		$@ &
	fi
}
# Just as the above, but if the process exists, restart it
run-or-restart() {
	if ! pgrep $1 ; then
		$@ &
	else
		process-restart $@
	fi
}

run picom &
wal -R &
run /usr/lib/jvm/java-14-openjdk/bin/java -Xmx1024m -jar /opt/xdman/xdman.jar -m &
run dunst &
run clipmenud &
run nm-applet &
# run mocp &
run volumeicon &
run mpd &
