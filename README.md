Functionality
-------------

`simple-bar-launcher` it's a simple launcher that shows on click (not on hover) on the left side
of the screen (location is not configurable yet). Works similar to [adeskbar](http://adeskbar.tuxfamily.org/) 
but only in one specific configuration, and it doesn't support plugins. It's an only launcher.

![simple-bar-launcher](docs/simple-bar-launcher.gif)

So why this is needed?
----------------------

As a long user of [adeskbar](http://adeskbar.tuxfamily.org/) as a launcher I'm used to the opening bar on click and because
I didn't find anything with similar functionality and adeskbar is not developed for a long time,
I wrote a simple launcher to fulfill this simple need.

Start from sources
------------------
Requires python 3.8+

```shell
git clone git@github.com:devqore/simple-bar-launcher.git
cd simple-bar-launcher
python -m venv venv
. venv/bin/activate
pip install -r requirements
python main.py
```

Run nightly binary
-------------------

```shell
sudo wget https://github.com/devqore/simple-bar-launcher/releases/download/nightly/simple-bar-launcher.linux.x86_64.bin -O /usr/local/bin/simple-bar-launcher
sudo chmod a+x /usr/local/bin/simple-bar-launcher
/usr/local/bin/simple-bar-launcher
```
Sample configuration
--------------------

Currently, only supported way of configuration `simple-bar-launcher` is using configuration file
`~/.config/simple-bar-launcher/config.yaml` as for example:

```yaml
icon_size: 44
hidden_width: 2
hide_timeout_msec: 900
layout_spacing: 5
launchers:
  - cmd: lutris
    icon: lutris
    name: Lutris
  - cmd: /usr/lib/firefox-developer-edition/firefox -P my-profile
    icon: firefox-developer-edition
    name: Firefox Developer Edition
  - cmd: slack
    icon: /usr/share/pixmaps/slack.png
    name: Slack
  - cmd: terminator
    icon: terminator
    name: Terminator
  - cmd: clementine
    icon: org.clementine_player.Clementine
    name: Clementine
```