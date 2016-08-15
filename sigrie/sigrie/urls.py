from django.conf.urls import patterns, include, url
from sigrie.settings import STATIC_ROOT

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns("",
	url(r"^admin/doc/", include("django.contrib.admindocs.urls")),
	url(r"^admin/", include(admin.site.urls)),
	#url(r"^static/(?P<path>.*)$", "django.views.static.serve", {"document_root": STATIC_ROOT}),
	#url(r"^latest", include("sigrie.additions.urls")),
	#url(r"^userdata", include("sigrie.userdata.urls")),
	url(r"^utils/talents?/$", "django.views.generic.simple.direct_to_template", {"template": "talents/index.html"}),


	#Uncomment the admin/doc line below to enable admin documentation:
	url(r"^admin/doc/", include("django.contrib.admindocs.urls")),

	#Uncomment the next line to enable the admin:
	url(r"^admin/", include(admin.site.urls)),

	url(r"^$", "sigrie.views.home", name="home"),
	url(r"^item/(?P<id>\d+)/$", "sigrie.views.model_single", {"model": "items"}, name="item_single"),
	url(r"^spells/$", "sigrie.spells.views.listing", name="spell_listing"),
	url(r"^spell/(?P<id>\d+)/$", "sigrie.views.model_single", {"model": "spells"}, name="spell_single"),
)
