# Generated by Django 3.0.4 on 2020-03-27 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ors', '0010_auto_20200327_1024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='number',
            field=models.IntegerField(unique=True),
        ),
    ]
