#!/bin/bash

#WINEPREFIX=$HOME/tmp/ wine /home/adys/bin/MPQEditor.exe /console Z:\\home\\adys\\src\\bzr\\wow-static\\extract-maps.mp2k
mv Interface interface
shopt -s globstar
rename 'y/A-Z/a-z/' interface/** &> /dev/null
rename 'y/A-Z/a-z/' interface/** &> /dev/null
rename 'y/A-Z/a-z/' interface/**
rm interface/worldmap/*.{blp,zmp}
rsync interface/worldmap/ maps -avP --delete # update maps dir
rm -rf interface
