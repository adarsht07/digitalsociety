from django.contrib import admin
from MemberApp.models import Event, Maintenance
from .models import *

# Register your models here.

admin.site.register(User)	
admin.site.register(Chairman)
