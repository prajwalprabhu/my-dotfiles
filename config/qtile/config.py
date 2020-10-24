# -*- coding: utf-8 -*-
import os
import socket
import subprocess
from libqtile.config import Key, Screen
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
# from typing import List  # noqa: F401

from groups import my_groups
from variable import mod
from key_binding import keys
from topbar import init_widgets_list
from colors import colors
from scratchpad import Scratchpad, DropDown_Keys
from rules import Rules


widget_defaults = dict(
    font="Ubuntu Mono",
    fontsize=12,
    padding=2,
    background=colors[2]
)


if __name__ in ["config", "__main__"]:
    screens = [
        Screen(top=bar.Bar(widgets=init_widgets_list(), opacity=1.0, size=20))]
    widgets_list = init_widgets_list()
    widgets_screen1 = init_widgets_list()
    scratchpad = Scratchpad()
    dd_keys = DropDown_Keys()
    groups = my_groups
    groups += scratchpad.init_scratchpad()
    keys += dd_keys.init_dropdown_keybindings()
    dgroups_key_binder = None
    # dgroups_app_rules = Rules().init_rules() # type: List
    main = None
    follow_mouse_focus = True
    bring_front_click = False
    cursor_warp = False
    auto_fullscreen = True
    focus_on_window_activation = "smart"
    extension_defaults = widget_defaults.copy()


@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])


# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
