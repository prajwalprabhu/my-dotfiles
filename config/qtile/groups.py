from libqtile.config import Group, Match
from libqtile import layout
import re
my_groups = [
    Group("SYS",
          layouts=[layout.Tile(), ]
          ),

    Group("WWW",
          layouts=[layout.Tile()],
          matches=[Match(wm_class=["firefox"])]
          ),
    Group("DEV",
          layouts=[layout.Tile(), layout.Max()],
          matches=[Match(wm_class="Code", wm_instance_class="code")]
          ),
    Group("DOC",
          layouts=[layout.Tile()],
          ),
    Group("VID",
          layouts=[layout.Tile()],
          ),
    Group("MUS",
          layouts=[layout.Tile()],
          ),
    Group("VBOX",
          layouts=[layout.Tile()],
          ),
    Group("OFC",
          layouts=[layout.Tile()],
          ),
    Group("FUN",
          layouts=[layout.Tile()],
          )
]
