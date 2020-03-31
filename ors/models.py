from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from kihivasok.models import Challenge
from taggit.managers import TaggableManager

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

def save_patrol_challenge(sender, instance, **kwargs):
    patrol = instance.patrol
    members = Patrolmember.objects.filter(patrol=patrol)
    challenge = instance.challenge
    for member in members:
        new_pmc = PatrolmemberChallenge.objects.create(nickname=member, challenge=challenge, status='N', times=0)

def delete_patrol_challenge(sender, instance, **kwargs):
    patrol = instance.patrol
    members = Patrolmember.objects.filter(patrol=patrol)
    challenge = instance.challenge
    for member in members:
        pmc = PatrolmemberChallenge.objects.get(nickname=member, challenge=challenge)
        pmc.delete()

post_save.connect(save_patrol_challenge, sender=PatrolChallenge)
post_delete.connect(delete_patrol_challenge, sender=PatrolChallenge)

class PatrolmemberChallenge(models.Model):
    STATUS_OPTIONS = (
        ('N', 'None'),
        ('A', 'Assigned'),
        ('F', 'Finished')
    )

    nickname = models.ForeignKey(Patrolmember, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUS_OPTIONS)
    times = models.IntegerField()

    class Meta:
        unique_together = ('nickname', 'challenge')
    
    def __str__(self):
        name = self.challenge.name + ' (' + self.nickname.nickname + ')'
        return name
