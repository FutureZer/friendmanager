from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('friendlist', views.friend_list, name='friends'),
    path('myrequests', views.sent_requests, name='myrequests'),
    path('received', views.received_requests, name='received')
]
