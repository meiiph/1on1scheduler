# Generated by Django 4.2 on 2024-03-13 20:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calendars', '0002_alter_invitation_is_accepted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='calendar',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='calendar',
            name='start_date',
        ),
    ]
