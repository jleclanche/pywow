# -*- coding: utf-8 -*-

from django.http import Http404
from django.shortcuts import render

def home(request):
	return render(request, "home.html")

def model_single(request, id, model):
	from pywow.environment import BuildNotFound, LocaleNotFound
	from pywow.game.tooltips import HtmlRenderer
	module = __import__("%s.%s" % ("sigrie", model))
	module = getattr(module, model)

	id = int(id)

	build = -1
	userBuild = request.GET.get("build")
	if userBuild and userBuild.isdigit():
		build = int(userBuild)

	locale = "enUS"
	userLocale = request.GET.get("locale")
	if userLocale and len(userLocale) == 4:
		locale = userLocale

	try:
		obj = module.cls(id, build, locale)
	except (BuildNotFound, LocaleNotFound):
		print "Invalid build/locale", build, locale
		obj = module.cls(id, -1, "enUS")
	except module.cls.DoesNotExist:
		raise Http404

	tooltip = obj.tooltip(HtmlRenderer)
	return render(request, "%s/single.html" % (model), {"obj": obj, "tooltip": tooltip})


def listing(request):
	return render(request, "common/listing.html")
