# Generated by Django 3.0.4 on 2020-03-22 17:33

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('kihivasok', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Kihivasok',
            new_name='Challenge',
        ),
    ]
