from django.contrib import admin
from .models import Patrol, Group, Patrolmember, PatrolChallenge, PatrolmemberChallenge

# Register your models here.
admin.site.register(Patrol)
admin.site.register(Group)
admin.site.register(Patrolmember)
admin.site.register(PatrolChallenge)
admin.site.register(PatrolmemberChallenge)