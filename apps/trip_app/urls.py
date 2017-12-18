from django.conf.urls import url
from . import views           # This line is new!

app_name = "trip_app"
urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^add$', views.add_trip, name = "add_trip"),
    url(r'^create$', views.create_trip, name = "create_trip"),
    url(r'^join/(?P<number>\d+)$', views.join_trip, name = "join_trip"),
    url(r'^destination/(?P<number>\d+)$', views.show_trip, name = "show_trip"),
    
  	url(r'^clear$', views.clear, name="clear"),
   
    ]