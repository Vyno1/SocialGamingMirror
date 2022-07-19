# Generated by Django 4.0.5 on 2022-07-19 13:07

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('levels_unlocked', models.IntegerField(default=0)),
                ('show_friend_info_screen', models.BooleanField(default=True)),
                ('steps', models.IntegerField(default=0)),
                ('scene', models.CharField(default='', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='WeatherTokens',
            fields=[
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='social_app.player')),
                ('token0', models.CharField(choices=[('sun', 'Sun'), ('rain', 'Rain'), ('wind', 'Wind'), ('thunder', 'Thunder'), ('snow', 'Snow'), ('none', 'None')], default='none', max_length=10)),
                ('token1', models.CharField(choices=[('sun', 'Sun'), ('rain', 'Rain'), ('wind', 'Wind'), ('thunder', 'Thunder'), ('snow', 'Snow'), ('none', 'None')], default='none', max_length=10)),
                ('token2', models.CharField(choices=[('sun', 'Sun'), ('rain', 'Rain'), ('wind', 'Wind'), ('thunder', 'Thunder'), ('snow', 'Snow'), ('none', 'None')], default='none', max_length=10)),
                ('token3', models.CharField(choices=[('sun', 'Sun'), ('rain', 'Rain'), ('wind', 'Wind'), ('thunder', 'Thunder'), ('snow', 'Snow'), ('none', 'None')], default='none', max_length=10)),
                ('token4', models.CharField(choices=[('sun', 'Sun'), ('rain', 'Rain'), ('wind', 'Wind'), ('thunder', 'Thunder'), ('snow', 'Snow'), ('none', 'None')], default='none', max_length=10)),
                ('current_weather', models.CharField(choices=[('sun', 'Sun'), ('rain', 'Rain'), ('wind', 'Wind'), ('thunder', 'Thunder'), ('snow', 'Snow'), ('none', 'None')], default='none', max_length=10)),
                ('date_of_last_daily_claim', models.DateField(default=datetime.date(1969, 1, 1))),
                ('used_shared', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='WaitingList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('waitinghost', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='waitinghost', to='social_app.player')),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guest_ready', models.BooleanField(default=False)),
                ('host_left', models.BooleanField(default=False)),
                ('guest_left', models.BooleanField(default=False)),
                ('host_skin', models.CharField(default='0', max_length=2)),
                ('guest_skin', models.CharField(default='0', max_length=2)),
                ('has_started', models.BooleanField(default=False)),
                ('is_over', models.BooleanField(default=False)),
                ('is_paused', models.BooleanField(default=False)),
                ('do_reset', models.BooleanField(default=False)),
                ('do_exit', models.BooleanField(default=False)),
                ('current_scene', models.CharField(default='', max_length=20)),
                ('sceneChanges', models.BooleanField(default=False)),
                ('friendship_is_updated', models.BooleanField(default=False)),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='host', to='social_app.player')),
                ('joined_player', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='joined', to='social_app.player')),
            ],
            options={
                'unique_together': {('host', 'joined_player')},
            },
        ),
        migrations.CreateModel(
            name='InviteMatch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accepted', models.BooleanField(default=False)),
                ('started', models.BooleanField(default=False)),
                ('Inviter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inviter', to='social_app.player')),
                ('invited_player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invited', to='social_app.player')),
            ],
            options={
                'unique_together': {('Inviter', 'invited_player')},
            },
        ),
        migrations.CreateModel(
            name='Friendship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.IntegerField(default=0)),
                ('mutual', models.BooleanField(default=False)),
                ('skins_unlocked', models.CharField(default='0000000000', max_length=10)),
                ('skin_drop_chance', models.FloatField(default=0.05)),
                ('step_multiplier', models.FloatField(default=1.0)),
                ('player1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friends', to='social_app.player')),
                ('player2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers', to='social_app.player')),
            ],
            options={
                'unique_together': {('player1', 'player2')},
            },
        ),
    ]
