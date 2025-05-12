from django.shortcuts import render, HttpResponse, redirect
from django.db.models import Q
from django.contrib import messages
from . import models
from django.http import JsonResponse
import json
from . import ai

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
                "tickets_total": len(models.Ticket.objects.all()),
                "activities": models.ActivityLog.get_all_activity(),
                "unread":models.Message.get_unread_count(user_id)
            }
            return render(request,'admin_dashboard.html',context)
        if user.role == 'staff':
            if user.department:
                total = user.department.dp_tickets.all()
                closed = user.department.dp_tickets.filter(status=3)
                open = user.department.dp_tickets.filter(status__in=[2, 4])
                context={
                    "user":user,
                    "ticket_closed":len(closed),
                    "ticket_open":len(user.department.dp_tickets.filter(status=2)),
                    "tickets_total":len(total),
                    "tickets_progress": len(user.department.dp_tickets.filter(status=4)),
                    "tickets":open,
                    "unread":models.Message.get_unread_count(user_id)

                }
            else:
                context={
                    "user":user,
                    "ticket_closed":0,
                    "ticket_open":0,
                    "tickets_total":0,
                    "tickets_progress": 0,
                    "tickets":[],
                    "unread":models.Message.get_unread_count(user_id)
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
    else:
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
                string = f" admin add a new department: {request.POST['department_name']}"
                models.ActivityLog.add_activity(string)
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
            'user':user,
            "unread":models.Message.get_unread_count(user_id)
        }
        return render (request,'user_create_ticket.html',context)
    else:
        return redirect('/landing')
    


def inbox(request):
    if 'user_id' in request.session:
        user_id=request.session['user_id']
        user=models.User.get_user_by_id(user_id)
        unread_messages = models.Message.objects.filter(user=user, is_read=False)
        unread_messages.update(is_read=True)
        context={
            'user':user,
            'user_messeges':user.messages.all(),
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
            'users':models.User.get_all_users(),
            "unread":models.Message.get_unread_count(user_id)
        }
        return render (request,'admin_users_page.html',context)
    else:
        return redirect('/landing')
    
def all_tickets(request):
    if 'user_id' in request.session:
        user_id=request.session['user_id']
        user=models.User.get_user_by_id(user_id)
        print(models.Message.get_unread_count(user_id))
        if user.role == 'admin':
            context={
                'user':user,
                'all_tickets':models.Ticket.show_tickets(),
                "unread":models.Message.get_unread_count(user_id)
            }
            return render (request,'admin_all_tickets.html',context)
        else:
            if user.role =='staff':
                context={
                    'user':user,
                    'all_tickets':models.Ticket.get_tickets_for_user_department(user_id),
                    "unread":models.Message.get_unread_count(user_id)
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
                user=models.User.get_user_by_id(request.session['user_id'])
                ticket=models.Ticket.create_ticket(request.POST)
                string = f"New ticket Created #{ticket.id} by user: {user.first_name} {user.last_name}"
                models.ActivityLog.add_activity(string)
                return redirect ('/dashboard')
        else:
            return redirect('/landing')
    else:
            return redirect('/landing')

def update_user(request):
    if 'user_id' in request.session:
        if request.method == 'POST':
            string = f"Admin updated user: {request.POST['first_name']} {request.POST['last_name']}"
            models.User.update_user(request.POST)
            models.ActivityLog.add_activity(string)
            return redirect ('/dashboard')
        else:
            return redirect('/landing')
    else:
            return redirect('/landing')
    
def delete_user(request):
    if 'user_id' in request.session:
        if request.method == 'POST':
            user = models.User.get_user_by_id(request.POST['user_id'])
            string = f"Admin deleted user: {user.first_name} {user.last_name}"
            models.User.delete_user(request.POST)
            models.ActivityLog.add_activity(string)
            return redirect ('/dashboard')
        else:
            return redirect('/landing')
    else:
            return redirect('/landing')

def change_user_role(request):
    if 'user_id' in request.session:
        if request.method == 'POST':
            user = models.User.get_user_by_id(request.POST['user_id'])
            string = f"Admin updated user: {user.first_name} {user.last_name} role to : {request.POST['role']}"
            models.ActivityLog.add_activity(string)
            models.User.update_user_role(request.POST)
            return redirect('/dashboard')
        else:
            return redirect('/landing')
    else:
            return redirect('/landing')
    
def assign_user_to_department(request):
    if 'user_id' in request.session:
        if request.method == 'POST':
            user = models.User.get_user_by_id(request.POST['user_id'])
            department = models.Department.git_departmen_by_id(request.POST['department_id'])
            string = f"Admin assigned user: {user.first_name} {user.last_name} to department : {department.name}"
            models.ActivityLog.add_activity(string)
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
            "unread":models.Message.get_unread_count(user.id)
        }
        return render(request,"ticket_info.html",context)
    else:
        return redirect('/landing')

def assign(request):
    if 'user_id' in request.session:
        if request.method == "POST":
            department = models.Department.git_departmen_by_id(request.POST['department_name'])
            string = f"Admin assigned ticket #{request.POST['ticket_id']} to department : {department.name}"
            models.ActivityLog.add_activity(string)
            models.Ticket.assign_ticket(request.POST)
            return redirect('/dashboard')
        else:
            return redirect('/landing')
    else:
        return redirect('/landing')
    
def close_ticket(request):
    if 'user_id' in request.session:
        if request.method == "POST":
            user = models.User.get_user_by_id(request.session['user_id'])
            string = f"Ticket #{request.POST['ticket_id']} was closed by staff: {user.first_name} {user.last_name} "
            models.ActivityLog.add_activity(string)
            models.Ticket.close_ticket(request.POST)
            return redirect('/dashboard')
        else:
            return redirect('/landing')
    else:
        return redirect('/landing')

def mark_inprogress(request):
    if 'user_id' in request.session:
        if request.method == "POST":
            user = models.User.get_user_by_id(request.session['user_id'])
            string = f"Ticket #{request.POST['ticket_id']} was marked in progress by user: {user.first_name} {user.last_name} "
            models.ActivityLog.add_activity(string)
            models.Ticket.mark_ticket(request.POST)
            return redirect('/dashboard')
        else:
            return redirect('/landing')
    else:
        return redirect('/landing')
    

def call_ai(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        description = data.get('description', '')
        json_data = ai.classify_ticket(description)
        department = models.Department.objects.filter(name=json_data['department']).first().id
        return JsonResponse({"priority":json_data['severity'].lower(), "department" :department})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def live_search(request):
    user = models.User.get_user_by_id(request.session['user_id'])
    query = request.GET.get('q', '')
    results = []

    if query:
        if user.role != "admin":
            tickets = user.department.dp_tickets.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )
        else:
            tickets = models.Ticket.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )
        results = [
            {
                'id': t.id,
                'title': t.title,
                'description': t.description,
                'status': t.status.name,
                'created_at': t.created_at,
                'location': t.issuer.location,
                'issuer':t.issuer.first_name,
                'assigned_to': "" if t.assigned_to is None else t.assigned_to.name
            }
            for t in tickets
        ]
    else:
        tickets = models.Ticket.objects.all()
        results = [
            {
                'id': t.id,
                'title': t.title,
                'description': t.description,
                'status': t.status.name,
                'created_at': t.created_at,
                'location': t.issuer.location,
                'issuer':t.issuer.first_name,
                'assigned_to': "" if t.assigned_to is None else t.assigned_to.name
            }
            for t in tickets
        ]
    
    return JsonResponse(list(results[::-1]), safe=False)