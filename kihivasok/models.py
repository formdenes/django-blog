from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager

# Create your models here.
class Challenge(models.Model):
    name = models.CharField(max_length=50)
    desc = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    tags = TaggableManager()
    promoted = models.BooleanField()
    thumb = models.ImageField(default="default.png", blank=True)
    created_by = models.ForeignKey(User, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def snippet(self):
        return self.desc[:200] + "..."

