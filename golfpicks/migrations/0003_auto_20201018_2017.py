# Generated by Django 3.1.1 on 2020-10-18 19:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('golfpicks', '0002_auto_20201018_1645'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='pick',
            unique_together={('event', 'punter')},
        ),
    ]
