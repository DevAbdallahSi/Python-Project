from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from . import models
import bcrypt
def index(request):
    return render (request,'index.html')

def register_form(request):
    if request.method == 'POST':
        errors = models.User.objects.basic_validator(request.POST)
        if errors:
            for k, v in errors.items():
                messages.error(request, v)
            return redirect('/')
        else:
            new=models.uesr_data(request.POST)
            request.session['user_id']=new
            return redirect ('/')
    else:
        return redirect ('/')
    
def login_page(request):
    if 'user_id' in request.session:
        context={
            'projects':models.all_project(),
            'user':models.get_user_by_id(request.session['user_id']),
        }
        return render(request, 'dashboard.html',context)
    else:
        return redirect('/')

def login_form(request):
    if request.method == 'POST':
        errors = models.UserManager.basic_validator_login(request.POST)
        if errors:
            for k, v in errors.items():
                messages.error(request, v)
            return redirect('/')
        else:
            user=models.UserManager.get_the_user_info(request.POST)
            if user:
                request.session['user_id']=user.id
                return redirect('/login_page')
            else:
                messages.error(request,'rong email or password')
                return redirect('/')
def logout(request):
    if 'user_id' in request.session:
        request.session.flush() 
        return redirect('/')