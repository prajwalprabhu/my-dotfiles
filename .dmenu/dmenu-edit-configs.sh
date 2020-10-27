#!/bin/bash
# Dmenu script for editing some of my more frequently edited config files.


declare options=("
bash
bspwm
dunst
dwm
i3
neovim
picom
polybar
spectrwm
st
termite
vifm
xresources
zsh
qtile 
awesome
quit")

choice=$(echo -e "${options[@]}" | dmenu -i -p 'Edit config file: ')

case "$choice" in
	quit)
		echo "Program terminated." && exit 1
	;;
	bash)
		choice="$HOME/.bashrc"
	;;
	bspwm)
		choice="$HOME/.config/bspwm/bspwmrc"
	;;
	dunst)
		choice="$HOME/.config/dunst/dunstrc"
	;;
	dwm)
		choice="$HOME/suckless/my-dwm/config.def.h"
	;;
	i3)
		choice="$HOME/.config/i3/config"
	;;
	neovim)
		choice="$HOME/.config/nvim/init.vim"
	;;
	picom)
		choice="$HOME/.config/picom/picom.conf"
	;;
	polybar)
		choice="$HOME/.config/polybar/config"
	;;
	st)
		choice="$HOME/suckless/st/config.def.h"
	;;
	termite)
		choice="$HOME/.config/termite/config"
	;;
	vifm)
		choice="$HOME/.config/vifm/vifmrc"
	;;
	xresources)
		choice="$HOME/.Xresources"
	;;
	zsh)
		choice="$HOME/.zshrc"
	;;
  qtile)
    choice="$HOME/.config/qtile/config.py"
  ;;
  awesome)
    choice="$HOME/.config/awesome/rc.lua"
  ;;
	*)
		exit 1
	;;
esac
st -e nvim "$choice"

