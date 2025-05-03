from django.urls import path
from . import views


urlpatterns = [
    path('',views.index),
    path('landing',views.landing),
    path('create_ticket',views.create_ticket),
    path('inbox',views.inbox),
    path('dashboard',views.dashboard),
    path('tickets',views.all_tickets),
    path('logout',views.logout),
    path('all_users',views.all_users),
    path('login',views.login_form)
]