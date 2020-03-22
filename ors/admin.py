from django.contrib import admin
from .models import Patrol, Group, Patrolmember

# Register your models here.
admin.site.register(Patrol)
admin.site.register(Group)
admin.site.register(Patrolmember)