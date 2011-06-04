#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from PIL import Image
from pilgrim.codecs import BLP
from sigrie.settings import MEDIA_ROOT

SIGRIE_TALENTS_PATH = MEDIA_ROOT + "img/wowtal/talents/backgrounds/"

coords = { # x,y coords for each part of the image
	"topleft": (0, 0),
	"topright": (256, 0),
	"bottomleft": (0, 256),
	"bottomright": (256, 256),
}

def main():
	talentframe_path = "talentframe/"
	images = {}
	
	for name in os.listdir(talentframe_path):
		print "Converting...", name
		key, pos = name.split("-")
		pos = pos.replace(".blp", "")
		if key not in images:
			images[key] = Image.new("RGBA", (300, 331))
		
		img = BLP(talentframe_path + name)
		images[key].paste(img, coords[pos])
	
	for name, img in images.items():
		img.save(SIGRIE_TALENTS_PATH + name + ".png")

if __name__ == "__main__":
	main()
