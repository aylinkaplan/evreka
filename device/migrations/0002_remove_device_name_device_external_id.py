# Generated by Django 5.0.7 on 2024-07-25 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='device',
            name='name',
        ),
        migrations.AddField(
            model_name='device',
            name='external_id',
            field=models.CharField(default='default', max_length=255, unique=True),
            preserve_default=False,
        ),
    ]
