#!/bin/sh

cat <<EOF | xmenu
|M|      centeredmaster  0   
><>      NULL            1
[M]      monocle         2
[]=      tile            3
>M>      centeredfloatingmaster  4 
[@]      spiral           5
[\\]     dwindle         6
HHH      grid            7
[D]      deck              8
[B]      bstack           9
EOF
