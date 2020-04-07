from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from accounts.models import Profile

# Create your models here.
class Challenge(models.Model):
    name = models.CharField(max_length=50)
    desc = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    tags = TaggableManager()
    promoted = models.BooleanField()
    add_to_patrol = models.BooleanField(default=True)
    thumb = models.ImageField(default="default.png", blank=True)
    creator = models.ForeignKey(Profile, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def snippet(self):
        if len(self.desc) <200:
            return self.desc
        return self.desc[:200] + "..."

class NewsPost(models.Model):
    header = models.CharField(max_length=100)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    actual = models.BooleanField()
    img = models.ImageField(blank=True)

    def __str__(self):
        return self.header