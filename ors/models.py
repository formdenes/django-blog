from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from kihivasok.models import Challenge

# Create your models here.
class Group(models.Model):
    number = models.IntegerField(unique=True)

    def __str__(self):
        return str(self.number)

class Patrol(models.Model):
    name = models.CharField(max_length=50)
    group_num = models.ForeignKey(Group, on_delete=models.CASCADE)
    group_leader = models.OneToOneField(User, default=None, on_delete=models.CASCADE)
    secret = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Patrolmember(models.Model):
    nickname = models.CharField(max_length=50)
    patrol = models.ForeignKey(Patrol, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('nickname', 'patrol')

    def __str__(self):
        return self.nickname

class PatrolChallenge(models.Model):
    patrol = models.ForeignKey(Patrol, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete = models.CASCADE)

    class Meta:
        unique_together = ('patrol', 'challenge')

    def __str__(self):
        pair = self.patrol.name + ' őrs - ' + self.challenge.name + ' kihívás'
        return pair
