# Generated by Django 4.0.5 on 2022-07-12 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_app', '0008_rename_player_friendship_player1_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='current_scene',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AddField(
            model_name='player',
            name='scene',
            field=models.CharField(default='', max_length=20),
        ),
    ]