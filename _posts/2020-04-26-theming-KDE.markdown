---
layout: post
title: "Theming KDE"
date: 2020-04-26
categories: workflow
excerpt: "I was about 13 when I built my first PC..."
header: 
  overlay_image: /assets/konsole.png
  overlay_filter: 0
---
## Introduction ##
I was about 13 when I built my first PC with a combination of savings,
birthday and christmas money, and help from a copious number of Youtube
tutorials. I still remember my panic when the internet didn't immediately work, and
I had to run out to TigerDirect to buy a WiFi adapter (whoops!). Since then I've
built about a dozen or so systems for family and friends, and found out I
wasn't alone - it seems to be a common beginner mistake to assume once you have
all the parts put together, the machine should just work like a prebuilt.

The other side of this is the $100 cost for a Windows installation disk. Turns
out there's no better way to turn a 13 year old into a Linux user than to ask
him for even more money after he's made the biggest purchase of his life. While
I eventually turned over the Microsoft tax (since Linux gaming support wasn't exactly
the best in 2013), I spent several weeks on Ubuntu 16.04 LTS, with the Gnome
desktop environment.

This first foray into Linux and FOSS was pretty huge for me. While I didn't
understand what I was doing then, using the command line to install drivers and
solving my own problems (while creating a good amount too!) was magical to me.
When I left for college and got my first laptop, I immediately dual-booted it
with Ubuntu 18.04 and Gnome.

This worked great for a while, and I steadily used Windows 10 less and less as I
got more used to the configurability and ease of use of Ubuntu and gnome. When I
started doing data science research with the Solar Durability and Lifetime
Extension center on campus, being familiar with Linux was a huge bonus. All of
the graduate students and PI's used Ubuntu and KDE, and the Raspberry Pi's we
primarily used to connect to the University's HPC were configured with Raspbian.

My laptop had a touchscreen, so I thought I was smart to be using Gnome with
its larger UI and (in my mind) more elegant design compared to the slow,
cluttered KDE environments I used on the HPC. But a friend of mine in the lab
showed me his XFCE setup and how deeply customized he had made it. It was around
this time that I switched to Manjaro just for the sake of more frequent updates
and better driver support on my Razer Blade Stealth, and I decided to make the
jump to KDE as well.

## The Setup ##
### Global Theme/Plasma Style ###
I use [Dracula] as my global theme. It's a fantastic dark color scheme, with a
lot of nice purples and greens, but perhaps most importantly, it exists for a
ton of applications. The dracula theme is consistent across my desktop
environment, my firefox top bar, my vim and konsole colors, etc. For the global
theme, I opened system settings -> Appearance -> Global Themes -> Get New Global
Themes.. and searched for it. I use it for my window decorations and Plasma
style as well, both in the Appearance tab as well in KDE's system settings.
![global theme](/assets/Screenshot_20200426_175508.png)
I've also tried out [Nordic], which is a gorgeous, more matte option. I prefer
Dracula, but I have no qualms recommending that one as well.

### Icons ###
For Icons, I use [Tela]. I really like how well the colors here pair with
Dracula. You can follow the link to the github for installation instructions,
but I just went from system settings -> Icons -> Get New Icons... since that was
easy.

### Other Fun Stuff ###
I love using virtual desktops to keep some semblance of order between my various
assignments and classes throughout the day. Often I'll have 4 desktops: one for
editing assignments and reading them from Canvas, one for textbook PDF's and
other reference material, one for reserve/putting other classwork out of mind,
and one for Spotify and whatever else is running in the background. I already
use hotkeys to open applications and for whatever is running, so having keys to
switch between desktops can get tricky. I much prefer the MacOS approach of
having decent touchpad support, but this isn't built into KDE/Manjaro.

I use [libinput-gestures] for this. Simply put, it lets you configure your
touchpad to recognize gesture inputs however you'd like. I followed it's install
guide to a T, installing the library from the AUR. I just use the defaults to
3-finger swipe between virtual desktops, but there's a ton of config options
detailed on the github.

On the desktop, I use [latte-dock], and specifically the Plasma layout. I've
tried it at the top and bottom, and prefer having as small a GUI as possible to
help me focus on whatever I'm working on. The bar is the least intrusive, most
intuitive metaphor for me, since I often find using pop-up panels gets annoying
when mousing around the screen. YMMV, of course.

#### Command Line Goodies ####
I really, really love the aesthetic and convenience of [yakuake]. It comes by
default on Manjaro KDE and makes interacting with the command line super easy. I
use Ctrl + Tab to bring it up, and F12 to fullscreen it (both set in System
Settings -> Shortcuts). If I'm coding alongside a tutorial or something like
that, I'll split screen with Konsole, but usually I prefer the drop-down.

Within the console, I use [tmux] to organize my workspace. Tmux is a terminal
multiplexer, which basically lets you interact with multiple instances of the
command line in one window. I might use 10% of its capabilities -- it's a hugely
useful app -- but I can't get by without it now. Ham Vocke has an awesome intro
to it on [his website] detailing how useful it is to him as a full-time
programmer. I'd strongly suggest that post and his follow-ups as an intro to
using the app. Here's a link to my current config file, which is largely poached
from various Reddit users and public github repos: 
[.tmux.conf](/assets/tmux.conf)

Within the command line, I replaced my prompt with [starship.rs], which is
wonderfully customizable. It lets me customize what the prompt looks like and
what information is included with it each time a command runs. I use it to
remind me what virtual environment I might be on, what git branch I'm on and
whether it's updated remotely, and get rough timings of commands.
![tmux and starship](/assets/Screenshot_20200426_182710.png)

And here's a link to my configuration file: [config](/assets/starship.toml) I
only use a small portion of the languages it can recognize. Checkout the
website for more!

Lastly, it's worth mentioning that I've themed out my Vim, Konsole, Firefox, and
tmux with the [Dracula] theme. Check out their documentation for installation of
each of these. Unfortunately, since the theme supports so many platforms, the
documentation is very general and I found myself going through a fair amount of
stackoverflow threads looking for small fixes (including spending about 20
minutes looking for a hidden file! fun times all around). Joking aside, I'll
link my .bashrc and .vimrc below for your utility/amusement:
[.bashrc](/assets/bashrc)
[.vimrc](/assets/vimrc)

[Dracula]: https://draculatheme.com/
[Tela]: https://github.com/vinceliuice/Tela-icon-theme
[libinput-gestures]: https://github.com/bulletmark/libinput-gestures
[latte-dock]: https://github.com/KDE/latte-dock
[tmux]: https://github.com/tmux/tmux
[his website]: https://www.hamvocke.com/blog/a-quick-and-easy-guide-to-tmux/
[starship.rs]: https://starship.rs/
[nordic]: https://github.com/EliverLara/Nordic
