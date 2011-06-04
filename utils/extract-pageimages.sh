#!/bin/bash

WINEPREFIX=$HOME/tmp wine /home/adys/bin/MPQEditor.exe /console Z:\\home\\adys\\src\\bzr\\wow-static\\extract-pageimages.mp2k
shopt -s globstar
rename 'y/A-Z/a-z/' pageimages/** &> /dev/null
rename 'y/A-Z/a-z/' pageimages/** &> /dev/null
rename 'y/A-Z/a-z/' pageimages/**
