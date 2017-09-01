from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns =[
		url(r'^$',views.index,name='index'),
		url(r'^logout/',views.logout, name='logout'),
		url(r'^summary/',views.summary, name='summary'),
		url(r'^applications/$',views.applications, name='applications'),
		url(r'^application/$',views.application, name='application'),
		# url(r'^application/(?P<ap_id>[0-9]+)$', name='application'),
		url(r'^response/',views.response, name='response'),
		url(r'^inbox/',views.inbox, name='inbox'),
		url(r'^(?P<ap_id>[0-9]+)/process/',views.process, name='process'),
		url(r'^(?P<ap_id>[0-9]+)/rep_request/',views.rep_request, name='rep_request'),
		url(r'^submit/',views.submit, name='submit'),
]
