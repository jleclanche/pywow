#!/bin/bash

WINEPREFIX=$HOME/tmp wine /home/adys/bin/MPQEditor.exe /console Z:\\home\\adys\\src\\bzr\\wow-static\\extract-icons.mp2k
rename 'y/A-Z/a-z/' icons/*
find icons -type f -size 0 | xargs rm -f
