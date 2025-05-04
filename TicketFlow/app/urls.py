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
    path('login',views.login_form),
    path('register',views.register_form),
    path('create_department',views.create_department),
    path('change_user_role',views.change_user_role),
    path('assign_user_to_department',views.assign_user_to_department),
    path('add_new_ticket',views.add_new_ticket),
    path('ticket/<int:ticket_id>',views.ticket_info),
    path('assign',views.assign),
    path('close_ticket',views.close_ticket),
    path('mark_inprogress',views.mark_inprogress)
]