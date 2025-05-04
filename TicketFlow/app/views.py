from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from . import models
from django.http import JsonResponse
import bcrypt

def index(request):
    return redirect ('/landing')

def dashboard(request):
    if 'user_id' in request.session:
        user_id=request.session['user_id']
        user=models.User.get_user_by_id(user_id)
        if user.role == 'admin':
            not_assigned = models.Ticket.show_tickets(1)
            closed = models.Ticket.show_tickets(3)
            open = models.Ticket.show_tickets(2)
            context={
                "user":user,
                "users":models.User.get_all_users(),
                "departments":models.Department.git_all_departmen(),
                "ticket_closed":len(closed),
                "ticket_open":len(open),
                "tickets":not_assigned,
                "tickets_total": len(models.Ticket.objects.all())
            }
            return render(request,'admin_dashboard.html',context)
        if user.role == 'staff':
            total = user.department.dp_tickets.all()
            closed = user.department.dp_tickets.filter(status=3)
            open = user.department.dp_tickets.filter(status__in=[2, 4])
            context={
                "user":user,
                "ticket_closed":len(closed),
                "ticket_open":len(user.department.dp_tickets.filter(status=2)),
                "tickets_total":len(total),
                "tickets_progress": len(user.department.dp_tickets.filter(status=4)),
                "tickets":open
            }
            return render(request,'departmint_dashborde.html',context)
        if user.role == 'user':
            context={
                "user":user,
                'user_tickets':models.Ticket.get_tickets_by_user_id(user_id)
            }
            return render(request,'user_dashboard.html',context)
    else:
        return redirect ('/landing')

def register_form(request):
    if request.method == 'POST':
        errors = models.User.objects.basic_validator(request.POST)
        if errors:
            for k, v in errors.items():
                messages.error(request, v)
            return redirect('/landing')
        else:
            new=models.User.register(request.POST)
            request.session['user_id']=new
            return redirect ('/landing')
    else:
        return redirect ('/landing')
    
def landing(request):
    if 'user_id' in request.session:
        return redirect('/dashboard')
    else:
        return render(request,'login_page.html')

def login_form(request):
    if request.method == 'POST':
        errors = models.User.objects.basic_validator_login(request.POST)
        if errors:
            for k, v in errors.items():
                messages.error(request, v)
            return redirect('/landing')
        else:
            user=models.User.get_the_user_info(request.POST)
            if user:
                request.session['user_id']=user.id
                return redirect('/dashboard')
            else:
                messages.error(request,'rong email or password')
                return redirect('/landing')
            
def logout(request):
    if 'user_id' in request.session:
        request.session.flush() 
        return redirect('/landing')
    
def create_department(request):
    if 'user_id' in request.session:
        if request.method == 'POST':
            errors = models.Department.objects.basic_validator(request.POST)
            if errors:
                for k, v in errors.items():
                    messages.error(request, v)
                return redirect('/landing')
            else:
                new_department=models.Department.create_department(request.POST)
                return redirect('/dashboard')
        else:
            return redirect('/landing')
    else:
            return redirect('/landing')

def create_ticket(request):
    if 'user_id' in request.session:
        user_id=request.session['user_id']
        user=models.User.get_user_by_id(user_id)
        context={
            'user':user
        }
        return render (request,'user_create_ticket.html',context)
    else:
        return redirect('/landing')
    


def inbox(request):
    if 'user_id' in request.session:
        user_id=request.session['user_id']
        user=models.User.get_user_by_id(user_id)
        if user.role != 'admin':
            context={
                'user':user,
                'user_messeges': user.messages.all(),
            }
            return render (request,'user_inbox.html',context)
        else:
            context={
                'user':user,
                'user_messeges':models.Message.show_messages(),
            }
            return render (request,'user_inbox.html',context)
    else:
        return redirect('/landing')

def all_users(request):
    if 'user_id' in request.session:
        user_id=request.session['user_id']
        user=models.User.get_user_by_id(user_id)
        context={
            'user':user,
            'users':models.User.get_all_users()
        }
        return render (request,'admin_users_page.html',context)
    else:
        return redirect('/landing')
    
def all_tickets(request):
    if 'user_id' in request.session:
        user_id=request.session['user_id']
        user=models.User.get_user_by_id(user_id)
        if user.role == 'admin':
            context={
                'user':user,
                'all_tickets':models.Ticket.show_tickets()
            }
            return render (request,'admin_all_tickets.html',context)
        else:
            if user.role =='staff':
                context={
                    'user':user,
                    'all_tickets':models.Ticket.get_tickets_for_user_department(user_id)
                }
                return render (request,'admin_all_tickets.html',context) 
            else:
                return redirect('/landing')
    else:
        return redirect('/landing')
    
def add_new_ticket(request):
    if 'user_id' in request.session:
        if request.method == 'POST':
            errors = models.Ticket.objects.validate_ticket(request.POST)
            if errors:
                for k, v in errors.items():
                    messages.error(request, v)
                return redirect('/landing')
            else:
                ticket=models.Ticket.create_ticket(request.POST)
                return redirect ('/dashboard')
        else:
            return redirect('/landing')
    else:
            return redirect('/landing')


def change_user_role(request):
    if 'user_id' in request.session:
        if request.method == 'POST':
            models.User.update_user_role(request.POST)
            return redirect('/dashboard')
        else:
            return redirect('/landing')
    else:
            return redirect('/landing')
    
def assign_user_to_department(request):
    if 'user_id' in request.session:
        if request.method == 'POST':
            models.User.update_user_department(request.POST)
            return redirect('/dashboard')
        else:
            return redirect('/landing')
    else:
            return redirect('/landing')
    
def ticket_info(request,ticket_id):
    if 'user_id' in request.session:
        user = models.User.get_user_by_id(request.session['user_id'])
        ticket =models.Ticket.get_ticket_by_id(ticket_id)
        context={
            "user":user,
            "ticket":ticket,
            "departments": models.Department.git_all_departmen(),
        }
        return render(request,"ticket_info.html",context)
    else:
        return redirect('/landing')

def assign(request):
    if 'user_id' in request.session:
        if request.method == "POST":
            models.Ticket.assign_ticket(request.POST)
            return redirect('/dashboard')
        else:
            return redirect('/landing')
    else:
        return redirect('/landing')
    
def close_ticket(request):
    if 'user_id' in request.session:
        if request.method == "POST":
            models.Ticket.close_ticket(request.POST)
            return redirect('/dashboard')
        else:
            return redirect('/landing')
    else:
        return redirect('/landing')

def mark_inprogress(request):
    if 'user_id' in request.session:
        if request.method == "POST":
            models.Ticket.mark_ticket(request.POST)
            return redirect('/dashboard')
        else:
            return redirect('/landing')
    else:
        return redirect('/landing')