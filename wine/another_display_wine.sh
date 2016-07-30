#!/bin/bash
X :2 -ac -terminate -config only_one_monitor.conf 
sleep 2
DISPLAY=:2 nice -20 env WINEPREFIX="~/.wine" wine $1