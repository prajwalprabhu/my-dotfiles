from libqtile.config import Key, Drag, Click
from libqtile.command import lazy
from variable import *
from functions import Function
from groups import my_groups
keys = [
    # The essentials
    Key([mod], "Return",
        lazy.spawn(myTerm),
        desc='Launches My Terminal'
        ),
    Key([mod, "shift"], "Return",
        lazy.spawn("dmenu_run -p 'Run: '"),
        desc='Dmenu Run Launcher'
        ),
    Key([mod], "Tab",
        lazy.next_layout(),
        desc='Toggle through layouts'
        ),
    Key([mod, "shift"], "c",
        lazy.window.kill(),
        desc='Kill active window'
        ),
    Key([mod, "shift"], "r",
        lazy.restart(),
        desc='Restart Qtile'
        ),
    Key([mod, "shift"], "q",
        lazy.shutdown(),
        desc='Shutdown Qtile'
        ),
    # Treetab controls
    Key([mod, "control"], "k",
        lazy.layout.section_up(),
        desc='Move up a section in treetab'
        ),
    Key([mod, "control"], "j",
        lazy.layout.section_down(),
        desc='Move down a section in treetab'
        ),
    # Window controls
    Key([mod], "k",
        lazy.layout.down(),
        desc='Move focus down in current stack pane'
        ),
    Key([mod], "j",
        lazy.layout.up(),
        desc='Move focus up in current stack pane'
        ),
    Key([mod, "shift"], "k",
        lazy.layout.shuffle_down(),
        desc='Move windows down in current stack'
        ),
    Key([mod, "shift"], "j",
        lazy.layout.shuffle_up(),
        desc='Move windows up in current stack'
        ),

    Key([mod], "Left",
        lazy.screen.prev_group(),
        desc="Go to Previous Group"
        ),
    Key([mod], "Right",
        lazy.screen.next_group(),
        desc="Go to Next Group"
        ),


    Key([mod], "h",
        lazy.layout.grow(),
        #  lazy.layout.increase_nmaster(),
        desc='Expand window (MonadTall), increase number in master pane (Tile)'
        ),
    Key([mod], "i",
        lazy.layout.increase_nmaster(),
        desc="increase master "
        ),
    Key([mod, "shift"], "i",
        lazy.layout.decrease_nmaster(),
        desc="increase master "
        ),
    Key([mod], "l",
        lazy.layout.shrink(),
        #  lazy.layout.decrease_nmaster(),
        desc='Shrink window (MonadTall), decrease number in master pane (Tile)'
        ),
    Key([mod], "n",
        lazy.layout.normalize(),
        desc='normalize window size ratios'
        ),

    Key([mod], "m",
        lazy.layout.maximize(),
        desc='toggle window between minimum and maximum sizes'
        ),
    Key([mod, "shift"], "f",
        lazy.window.toggle_floating(),
        desc='toggle floating'
        ),
    Key([mod, "shift"], "m",
        lazy.window.toggle_fullscreen(),
        desc='toggle fullscreen'
        ),
    # Stack controls
    Key([mod, "shift"], "space",
        lazy.layout.rotate(),
        lazy.layout.flip(),
        desc='Switch which side main pane occupies (XmonadTall)'
        ),
    Key([mod], "space",
        lazy.layout.next(),
        desc='Switch window focus to other pane(s) of stack'
        ),
    Key([mod, "control"], "Return",
        lazy.layout.toggle_split(),
        desc='Toggle between split and unsplit sides of stack'
        ),
    Key([alt], "b",
        lazy.spawn(myBrowser),
        desc=f"Launches {myBrowser}"
        ),
    Key([alt], "c",
        lazy.spawn("clipmenu"),
        desc="Launches Clipmenu"
        ),
    #  Key([alt],"m",
    #        lazy.spawn(tdrop+"-n 2 -a st -e mocp"),
    #        desc="Launches mocp"),
    # #  Key([alt],"Return",
    #       lazy.spawn(tdrop+"-n 1 -a st"),
    #       desc="Launches st"),
    Key([alt], "v",
        lazy.spawn("code"),
        desc="VS-code"),
    Key([alt], "f",
        lazy.spawn("st -e vifmrun"),
        desc="Vifm"),
    Key([], "XF86AudioRaiseVolume",
        lazy.spawn("pamixer -i 5"),
        desc="Increase Volume"),
    Key([], "XF86AudioLowerVolume",
        lazy.spawn("pamixer -d 5"),
        desc="Decrease Volume"),

    Key([], "XF86AudioMute",
        lazy.spawn("pamixer -t"),
        desc="Toggle Mute"),
    Key([], "XF86AudioNext",
        lazy.spawn(
        "mocp -f ; sleep 1 ; name=$(mocp -Q %file) ; notify-send $name"),
        desc="Next Song MOCP"),
    Key([], "XF86AudioPrev",
        lazy.spawn(
        "mocp -r ; sleep 1 ;name=$(mocp -Q %file); notify-send $name"),
        desc="Audio Previous in MOCP"),
    Key([], "XF86AudioPlay",
        lazy.spawn(" mocp -G"),
        desc="Toggle Pause in MOCP"),

    Key([mod], "Home",
        lazy.window.bring_to_front()),				# Bring window to front
    Key([mod, "control"], "Return",
        lazy.window.toggle_floating()),				# Toggle floating

    Key([mod, "shift"], "Left",
        Function.window_to_prev_group()),			# Move window to previous group
    Key([mod, "shift"], "Right",
        Function.window_to_next_group()),			# Move window to next group


]

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

for i, group in enumerate(my_groups, 1):
    # Switch to another group
    keys.append(Key([mod], str(i), lazy.group[group.name].toscreen()))
    # Send current window to another group
    keys.append(Key([mod, "shift"], str(i), lazy.window.togroup(group.name)))
