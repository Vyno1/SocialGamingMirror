# Generated by Django 4.0.5 on 2022-07-13 10:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social_app', '0009_alter_weathertokens_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='weathertokens',
            name='friend_token',
        ),
    ]