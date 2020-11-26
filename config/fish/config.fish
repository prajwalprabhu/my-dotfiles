set -x PATH $PATH ~/.local/bin
set EDITOR 'nvim'
alias aup="pamac upgrade --aur"
alias grubup="sudo update-grub"
alias orphaned="sudo pacman -Rns (pacman -Qtdq)"
alias fixpacman="sudo rm /var/lib/pacman/db.lck"
alias ls='ls --color=auto'
alias la='ls -a'
alias ll='ls -la'
alias l='ls'
alias l.="ls -A | egrep '^\.'"
alias grep='grep --color=auto'
alias egrep='egrep --color=auto'
alias fgrep='fgrep --color=auto'
alias df='df -h'
alias unlock="sudo rm /var/lib/pacman/db.lck"
alias free="free -mt"
alias uac="sh ~/.bin/main/000*"
alias wget="wget -c"
alias userlist="cut -d: -f1 /etc/passwd"
alias merge="xrdb -merge ~/.Xresources"
alias pacman='sudo pacman --color auto'
alias update='sudo pacman -Syyu'
alias pksyua="yay -Syu --noconfirm"
alias upall="yay -Syu --noconfirm"
alias psa="ps auxf"
alias psgrep="ps aux | grep -v grep | grep -i -e VSZ -e"
alias update-grub="sudo grub-mkconfig -o /boot/grub/grub.cfg"
alias update-fc='sudo fc-cache -fv'
alias hw="hwinfo --short"
alias yayskip='yay -S --mflags --skipinteg'
alias trizenskip='trizen -S --skipinteg'
alias microcode='grep . /sys/devices/system/cpu/vulnerabilities/*'
alias mirror="sudo reflector -f 30 -l 30 --number 10 --verbose --save /etc/pacman.d/mirrorlist"
alias mirrord="sudo reflector --latest 50 --number 20 --sort delay --save /etc/pacman.d/mirrorlist"
alias mirrors="sudo reflector --latest 50 --number 20 --sort score --save /etc/pacman.d/mirrorlist"
alias mirrora="sudo reflector --latest 50 --number 20 --sort age --save /etc/pacman.d/mirrorlist"
alias yta-aac="youtube-dl --extract-audio --audio-format aac "
alias yta-best="youtube-dl --extract-audio --audio-format best "
alias yta-flac="youtube-dl --extract-audio --audio-format flac "
alias yta-m4a="youtube-dl --extract-audio --audio-format m4a "
alias yta-mp3="youtube-dl --extract-audio --audio-format mp3 "
alias yta-opus="youtube-dl --extract-audio --audio-format opus "
alias yta-vorbis="youtube-dl --extract-audio --audio-format vorbis "
alias yta-wav="youtube-dl --extract-audio --audio-format wav "
alias ytv-best="youtube-dl -f bestvideo+bestaudio "
alias rip="expac --timefmt='%Y-%m-%d %T' '%l\t%n %v' | sort | tail -200 | nl"
alias riplong="expac --timefmt='%Y-%m-%d %T' '%l\t%n %v' | sort | tail -3000 | nl"
alias cleanup='sudo pacman -Rns (pacman -Qtdq)'
alias jctl="journalctl -p 3 -xb"
alias nlightdm="sudo nano /etc/lightdm/lightdm.conf"
alias npacman="sudo nano /etc/pacman.conf"
alias ngrub="sudo nano /etc/default/grub"
alias nmkinitcpio="sudo nano /etc/mkinitcpio.conf"
alias nslim="sudo nano /etc/slim.conf"
alias noblogout="sudo nano /etc/oblogout.conf"
alias nmirrorlist="sudo nano /etc/pacman.d/mirrorlist"
alias nconfgrub="sudo nano /boot/grub/grub.cfg"
alias gpg-check="gpg2 --keyserver-options auto-key-retrieve --verify"
alias gpg-retrieve="gpg2 --keyserver-options auto-key-retrieve --receive-keys"
alias ssn="sudo shutdown now"
alias sr="sudo reboot"
alias ..='cd ..' 
alias ...='cd ../..'
alias .3='cd ../../..'
alias .4='cd ../../../..'
alias .5='cd ../../../../..'
alias cp="cp -i"
alias mv='mv -i'
alias mi="sudo make install"
alias addup='git add -u'
alias gaa='git add -A'
alias branch='git branch'
alias checkout='git checkout'
alias clone='git clone'
alias commit='git commit -m'
alias fetch='git fetch'
alias pull='git pull origin'
alias push='git push origin'
alias gs='git status'
alias newtag='git tag -a'
alias gac="git commit -a"
alias erc='nvim ~/.config/fish/conf.d/omf.fish'
alias pm="pacman "
alias clr="clear"
alias vf="~/.config/vifm/scripts/vifmrun"
alias gt="~/go/bin/tour"
alias kite="~/.local/share/kite/kited"
alias erl="nvim ~/.config/awesome/rc.lua"
alias gr="cd ~/repo"
alias gmd="cd ~/repo/my-dotfiles"
alias tdrop="tdrop -h 70% -w 60% -x 20% -y 15%"
alias ls="lsd" 
function c++
    g++ $argv[1] -o $argv[2] ; ./$argv[2] 
end
function locate
    find $argv[1] -name $argv[2] 2>/dev/null
end
neofetch


