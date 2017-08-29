from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns =[
		url(r'^$',views.index,name='index'),
		url(r'^logout/',views.logout, name='logout'),
		url(r'^summary/',views.summary, name='summary'),
		url(r'^application/',views.application, name='application'),
		url(r'^response/',views.response, name='response'),
		# url(r'^submit/',views.submit, name='submit')

]
