from django.http import Http404
from django.shortcuts import render
from pywow.game.tooltips import HtmlRenderer
from pywow.game.items import Item

def listing(request):
	return render(request, "common/listing.html")

def single(request, id):
	id = int(id)
	obj = Item(id)
	tooltip = obj.tooltip(HtmlRenderer)
	return render(request, "spells/single.html", {"obj": obj, "tooltip": tooltip})
