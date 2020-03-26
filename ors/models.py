from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

# Create your models here.
class Group(models.Model):
    number = models.IntegerField()

    def __str__(self):
        return str(self.number)

class Patrol(models.Model):
    name = models.CharField(max_length=50)
    group_num = models.ForeignKey(Group, on_delete=models.CASCADE)
    group_leader = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    secret = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Patrolmember(models.Model):
    nickname = models.CharField(max_length=50)
    patrol = models.ForeignKey(Patrol, on_delete=models.CASCADE)

    def __str__(self):
        return self.nickname
