from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group_num = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return "%s (%s)" % (self.user.username , self.group_num)