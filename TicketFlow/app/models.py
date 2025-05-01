from django.db import models

# Create your models here.

class TicketManager(models.Manager):
    def validate_ticket(self, postData):
        errors = {}
        if len(postData['title']) < 2:
            errors['title'] = "Title must be at least 2 characters"
        if len(postData['description']) < 15:
            errors['description'] = "Description must be at least 15 characters"
        return errors
 
