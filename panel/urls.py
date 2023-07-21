#from django.conf.urls import url
from django.urls import path
from django.conf import settings

from . import views

app_name = 'panel'

urlpatterns = [
    path('', views.index, name="index" ),

    path('users/change-password/', views.change_password, name="change_password"),
    path('api/users/change-password/', views.api_users_change_password, name="api_users_change_password"),

    # Logout
    path('logout/', views.logout_, name="logout"),
]


