# Generated by Django 4.0.5 on 2022-07-13 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_app', '0010_remove_weathertokens_friend_token'),
    ]

    operations = [
        migrations.RenameField(
            model_name='friendship',
            old_name='player',
            new_name='player1',
        ),
        migrations.RenameField(
            model_name='friendship',
            old_name='friend',
            new_name='player2',
        ),
        migrations.AlterUniqueTogether(
            name='friendship',
            unique_together={('player1', 'player2')},
        ),
        migrations.AddField(
            model_name='friendship',
            name='step_multiplier',
            field=models.FloatField(default=1.0),
        ),
        migrations.AddField(
            model_name='match',
            name='current_scene',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AddField(
            model_name='match',
            name='sceneChanges',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='player',
            name='scene',
            field=models.CharField(default='', max_length=20),
        ),
    ]