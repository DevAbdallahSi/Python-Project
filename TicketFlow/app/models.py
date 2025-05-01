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
    def basic_validator_login(post):
        errors = {}
        if not EMAIL_REGEX.match(post['email_log']):    # test whether a field matches the pattern            
            errors['email_log'] = "Invalid email address!"
        return errors

class TicketManager(models.Manager):
    def validate_ticket(self, postData):
        errors = {}
        if len(postData['title']) < 2:
            errors['title'] = "Title must be at least 2 characters"
        if len(postData['description']) < 15:
            errors['description'] = "Description must be at least 15 characters"
        return errors
    
class DepartmentManager(models.Manager):
    def basic_validator(self, post):
        errors = {}
        if len(post['name']) <= 2:
            errors["name"] = " name should be at least 2 characters"
        if len(post['description']) < 5:
            errors["description"] = " description should be at least 2 characters"
        return errors
class Department(models.Model):
    name=models.CharField(max_length=50)
    desc=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    role=models.CharField(max_length=50)
    location=models.CharField(max_length=50)
    google_id=models.CharField(max_length=255)
    department=models.ForeignKey(Department,related_name='users')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects=UserManager()

    def uesr_data(post):
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
        

class Messages(models.Model):
    content=models.TextField()
    comment=models.TextField()
    user=models.ForeignKey(User,related_name='messages')
    department=models.ForeignKey(Department,related_name='department_messages')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Status(models.Model):
    name = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Ticket(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    priority = models.CharField(max_length=20)
    status = models.ForeignKey(Status,related_name="status_tickets")
    issuer = models.ForeignKey(User,related_name="user_tickets")
    assigned_to = models.ForeignKey(Department,related_name="dp_tickets")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects=TicketManager()

