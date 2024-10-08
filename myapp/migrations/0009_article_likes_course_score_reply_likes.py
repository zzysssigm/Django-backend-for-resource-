# Generated by Django 5.0.8 on 2024-08-10 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='likes',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='course',
            name='score',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=3),
        ),
        migrations.AddField(
            model_name='reply',
            name='likes',
            field=models.IntegerField(default=0),
        ),
    ]
