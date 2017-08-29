from django.conf.urls import url, include
from django.contrib import admin
from basic import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',views.index,name='index'),
    url(r'^login/',views.login, name='login'),
    url(r'^logout/',views.logout, name='logout'),
    url(r'^leave_module/', include('leavemodule.urls')),
    url(r'^enter/',views.enter,name='enter'),
    url(r'^enter1/',views.enter1,name='enter1')

]
