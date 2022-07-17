# Generated by Django 4.0.5 on 2022-07-01 09:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('social_app', '0003_friendship_skin1_unlocked_friendship_skin2_unlocked'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='friendship',
            name='skin1_unlocked',
        ),
        migrations.RemoveField(
            model_name='friendship',
            name='skin2_unlocked',
        ),
        migrations.RemoveField(
            model_name='match',
            name='position',
        ),
        migrations.RemoveField(
            model_name='match',
            name='velocity_x',
        ),
        migrations.RemoveField(
            model_name='match',
            name='velocity_y',
        ),
        migrations.AddField(
            model_name='friendship',
            name='skin_drop_chance',
            field=models.FloatField(default=0.05),
        ),
        migrations.AddField(
            model_name='friendship',
            name='skins_unlocked',
            field=models.CharField(default='0000000000', max_length=10),
        ),
        migrations.AddField(
            model_name='match',
            name='joined_player',
            field=models.OneToOneField(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='joined', to='social_app.player'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='match',
            name='host',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='host', to='social_app.player'),
        ),
        migrations.CreateModel(
            name='WeatherTokens',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token0', models.CharField(choices=[('sun', 'Sun'), ('rain', 'Rain'), ('wind', 'Wind'), ('thunder', 'Thunder'), ('snow', 'Snow'), ('none', 'None')], default='none', max_length=10)),
                ('token1', models.CharField(choices=[('sun', 'Sun'), ('rain', 'Rain'), ('wind', 'Wind'), ('thunder', 'Thunder'), ('snow', 'Snow'), ('none', 'None')], default='none', max_length=10)),
                ('token2', models.CharField(choices=[('sun', 'Sun'), ('rain', 'Rain'), ('wind', 'Wind'), ('thunder', 'Thunder'), ('snow', 'Snow'), ('none', 'None')], default='none', max_length=10)),
                ('token3', models.CharField(choices=[('sun', 'Sun'), ('rain', 'Rain'), ('wind', 'Wind'), ('thunder', 'Thunder'), ('snow', 'Snow'), ('none', 'None')], default='none', max_length=10)),
                ('token4', models.CharField(choices=[('sun', 'Sun'), ('rain', 'Rain'), ('wind', 'Wind'), ('thunder', 'Thunder'), ('snow', 'Snow'), ('none', 'None')], default='none', max_length=10)),
                ('friend_token', models.CharField(choices=[('sun', 'Sun'), ('rain', 'Rain'), ('wind', 'Wind'), ('thunder', 'Thunder'), ('snow', 'Snow'), ('none', 'None')], default='none', max_length=10)),
                ('current_weather', models.CharField(choices=[('sun', 'Sun'), ('rain', 'Rain'), ('wind', 'Wind'), ('thunder', 'Thunder'), ('snow', 'Snow'), ('none', 'None')], default='none', max_length=10)),
                ('received_daily_token', models.BooleanField(default=False)),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='social_app.player')),
            ],
        ),
    ]