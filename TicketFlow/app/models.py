from django.db import models

# Create your models here.
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

