from os import environ
from libqtile.config import ScratchPad, DropDown, Key
from libqtile.command import lazy

class Scratchpad(object):

	def init_scratchpad(self):

		# Terminal
		# terminal = environ.get("TERMINAL_SOLO")
        # terminal=myTerm
        # terminal=myTerm
		# Configuration
		height =				0.4650
		y_position =			0.0151
		warp_pointer =			False
		on_focus_lost_hide =	True
		opacity =				1

		return [
			ScratchPad("SPD",
				dropdowns = [
					# Drop down terminal with tmux session
					DropDown("term",
						# terminal + " -e tmux new-session -A -s 'dd'",
                        'st',
						opacity = opacity,
						y = y_position,
						height = height,
						on_focus_lost_hide = on_focus_lost_hide,
						warp_pointer = warp_pointer),

					# Another terminal exclusively for music player
					DropDown("music",
						"st  -e mocp",
						opacity = opacity,
						y = y_position,
						height = height,
						on_focus_lost_hide = on_focus_lost_hide,
						warp_pointer = warp_pointer),

					# Another terminal exclusively for qshell
					DropDown("qshell",
						 "st -e qshell",
						opacity = opacity,
						y = y_position,
						height = height,
						on_focus_lost_hide = on_focus_lost_hide,
						warp_pointer = warp_pointer)
				]
			),
		]

class DropDown_Keys(object):

	##### DROPDOWNS KEYBINDINGS #####

	def init_dropdown_keybindings(self):

		# Key alias
		mod =	"mod4"
		alt =	"mod1"
		altgr =	"mod5"

		return [
			Key([alt], "Return",
				lazy.group["SPD"].dropdown_toggle("term")),
			Key([alt], "m",
				lazy.group["SPD"].dropdown_toggle("music")),
			Key([mod], "semicolon",
				lazy.group["SPD"].dropdown_toggle("qshell")),
		]

# vim: tabstop=4 shiftwidth=4 noexpandtab