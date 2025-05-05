from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class UserManager(models.Manager):
    def basic_validator(self, post):
        errors = {}
        if not all([post['first_name'], post['last_name'], post['email'], post['password'],post['confirm_pw']]):
            errors["required"] = "All fields are required"
        if len(post['first_name']) < 2 or len(post['last_name']) < 2:
            errors["required_name"] = "First and Last name must each be at least 2 characters long."
        if len(post['password']) <= 8:
            errors["password"] = " password should be at least 8 characters"
        if post['password'] != post['confirm_pw']:
            errors['password_match'] = "Passwords must match"
        if not EMAIL_REGEX.match(post['email']):    # test whether a field matches the pattern            
            errors['email'] = "Invalid email address!"
        if User.objects.filter(email=post['email']).exists():
            errors['email'] = 'email is already exists'
        return errors
    def basic_validator_login(self,post):
        errors = {}
        if not EMAIL_REGEX.match(post['email_log']):    # test whether a field matches the pattern            
            errors['email_log'] = "Invalid email address!"
        return errors

class TicketManager(models.Manager):
    def validate_ticket(self, postData):
        errors = {}
        if len(postData['title']) < 2:
            errors['title'] = "Title must be at least 2 characters"
        if len(postData['description']) < 5:
            errors['description'] = "Description must be at least 5 characters"
        return errors
    
class DepartmentManager(models.Manager):
    def basic_validator(self, post):
        errors = {}
        if len(post['department_name']) < 2:
            errors["department_name"] = " name should be at least 2 characters"
        if len(post['description']) < 5:
            errors["description"] = " description should be at least 5 characters"
        return errors
    
class Department(models.Model):
    name=models.CharField(max_length=50)
    desc=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects=DepartmentManager()

    def create_department(post):
        name=post['department_name']
        desc=post['description']
        new_department=Department.objects.create(name=name,desc=desc)
        return new_department.id
    def git_all_departmen():
        return Department.objects.all()
    
    def git_departmen_by_id(id):
        return Department.objects.get(id=id)


class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    role=models.CharField(max_length=50 ,default='user')
    location=models.CharField(max_length=50 ,default='Ramallah')
    google_id=models.CharField(max_length=255,null=True, blank=True)
    department=models.ForeignKey(Department,related_name='users',on_delete=models.CASCADE ,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects=UserManager()
    

    def register(post):
        hashed_pw = bcrypt.hashpw(post['password'].encode(), bcrypt.gensalt()).decode()
        first_name=post['first_name']
        last_name=post['last_name']
        email=post['email']
        new=User.objects.create(first_name=first_name,last_name=last_name,email=email,password=hashed_pw)
        return new.id

    def get_user_by_id(user_id):
        return User.objects.get(id=user_id)
    
    def get_the_user_info(post):
        email_log = post['email_log']
        password = post['password']
        user = User.objects.filter(email=email_log).first()
        if user and bcrypt.checkpw(password.encode(), user.password.encode()):
            return user
        else:
            return None
    
    def update_user_role(post):
        user = User.objects.get(id=post["user_id"])
        user.role = post["role"]
        user.save()

    def update_user_department(post):
        user = User.objects.get(id=post["user_id"])
        department = Department.objects.get(id=post["department_id"])
        user.department = department
        user.save()

    def update_user(post):
        user = User.objects.get(id=post["user_id"])
        user.first_name = post['first_name']
        user.last_name = post['last_name']
        user.email = post['email']
        user.save()
    
    def delete_user(post):
        user = User.objects.get(id=post["user_id"])
        user.delete()

    def get_all_users():
        return User.objects.all()

class Message(models.Model):
    content=models.TextField()
    comment=models.TextField()
    user=models.ForeignKey(User,related_name='messages',on_delete=models.CASCADE)
    department=models.ForeignKey(Department,related_name='department_messages',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def create_messages(post):
        user = User.objects.get(id=post['issuer_id'])
        department = Department.objects.get(id=post['department_id'])
        content=post['message_content']
        comment=post['comment']
        message = Message.objects.create(content=content,comment=comment,user=user,department=department)
        return message

    def show_messages():
        return Message.objects.all()
    
class Status(models.Model):
    name = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def create_status(post):
        name =post['name']
        status= Status.objects.create(name=name)
        return status

    def show_status():
        return Status.objects.all()
    
    
class Ticket(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    priority = models.CharField(max_length=20 ,null=True, blank=True)
    status = models.ForeignKey(Status,related_name="status_tickets",on_delete=models.CASCADE)
    issuer = models.ForeignKey(User,related_name="user_tickets",on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(Department,related_name="dp_tickets",on_delete=models.CASCADE ,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects=TicketManager()

    
    def create_ticket(post):
        title = post['title']
        description = post['description']
        status = Status.objects.get(id=1)
        issuer = User.objects.get(id=post['user_id'])
        ticket = Ticket.objects.create(title=title, description=description, status=status, issuer=issuer)
        return ticket

    def show_tickets(status=None):
        if status:
            return Ticket.objects.filter(status=status)
        else:
            return Ticket.objects.all()
    
    def assign_ticket(post):
        ticket = Ticket.objects.get(id=post['ticket_id'])
        ticket.priority = post['priority']
        ticket.assigned_to = Department.objects.get(id=post['department_name'])
        ticket.status = Status.objects.get(id=2)
        ticket.save()

    def get_ticket_by_id(ticket_id):
        return Ticket.objects.get(id=ticket_id)
    
    def get_tickets_by_user_id(user_id):
        return Ticket.objects.filter(issuer_id=user_id)
    
    def get_tickets_for_user_department(user_id):
        user = User.objects.get(id=user_id)
        return Ticket.objects.filter(assigned_to=user.department)
    
    def close_ticket(post):
        Message.create_messages(post)
        ticket = Ticket.objects.get(id=post['ticket_id'])
        ticket.status = Status.objects.get(id=3)
        ticket.save()
    
    def mark_ticket(post):
        ticket = Ticket.objects.get(id=post['ticket_id'])
        ticket.status = Status.objects.get(id=4)
        ticket.save()

class ActivityLog(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def add_activity(string):
        ActivityLog.objects.create(message=string)
    
    def get_all_activity():
        return ActivityLog.objects.all()