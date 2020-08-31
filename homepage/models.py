from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class CustomUser(AbstractUser):
    def __str__(self):
       return self.username
    pass

class Ticket(models.Model):
    NEW = 'New'
    IN_PROGRESS = 'In Progress'
    DONE = 'Done'
    INVALID = 'Invalid'
    title = models.CharField(max_length=80)
    time_created = models.DateTimeField()
    description = models.TextField()
    filer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status_choices = [
        (NEW, 'New'),
        (IN_PROGRESS, 'In Progress'),
        (DONE, 'Done'),
        (INVALID, 'Invalid')
    ]
    status = models.CharField(max_length=11, choices=status_choices, default='NEW')
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name='assignee')
    completed_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name='fixed_by')

    def __str__(self):
        return self.title
