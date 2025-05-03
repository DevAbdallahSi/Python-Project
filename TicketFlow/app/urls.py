from django.urls import path
from . import views


urlpatterns = [
    path('',views.index),
    path('/landing',views.landing),
    path('/create_ticket',views.index),
    path('/inbox',views.index),
    path('/dashboard',views.index),
    path('/tickets',views.index),
]