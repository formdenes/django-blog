from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    group = models.ForeignKey(to='ors.Group', on_delete=models.CASCADE, default=2)
    patrol = models.CharField(max_length=50, default="Alma")
    secret = models.CharField(max_length=30, default=None, blank=True, null=True)

    def __str__(self):
        return "%s" % (self.user.username)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()
