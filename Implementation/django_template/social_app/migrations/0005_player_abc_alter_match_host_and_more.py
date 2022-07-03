# Generated by Django 4.0.5 on 2022-07-03 10:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('social_app', '0004_remove_friendship_skin1_unlocked_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='abc',
            field=models.CharField(default=0, max_length=20),
        ),
        migrations.AlterField(
            model_name='match',
            name='host',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='host', to='social_app.player'),
        ),
        migrations.AlterField(
            model_name='match',
            name='joined_player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='joined', to='social_app.player'),
        ),
    ]
