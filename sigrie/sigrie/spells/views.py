from django.http import Http404
from django.shortcuts import render
from pywow.game.tooltips import HtmlRenderer
from pywow.game.spells import Spell

def listing(request):
	return render(request, "common/listing.html")
