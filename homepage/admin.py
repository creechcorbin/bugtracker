from django.contrib import admin
from homepage.models import CustomUser, Ticket

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Ticket)