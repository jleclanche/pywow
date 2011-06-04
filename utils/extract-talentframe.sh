#!/bin/bash

WINEPREFIX=$HOME/tmp wine /home/adys/bin/MPQEditor.exe /console Z:\\home\\adys\\src\\bzr\\wow-static\\extract-talentframe.mp2k
rename 'y/A-Z/a-z/' talentframe/*
rm talentframe/ui-* talentframe/talentframe-rankborder.blp
