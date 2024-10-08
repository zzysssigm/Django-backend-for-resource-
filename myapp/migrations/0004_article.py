# Generated by Django 5.0.6 on 2024-08-02 15:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_remove_user_cookie'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('article_id', models.AutoField(primary_key=True, serialize=False)),
                ('article_title', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('tags', models.CharField(max_length=255)),
                ('stars', models.IntegerField(default=0)),
                ('views', models.IntegerField(default=0)),
                ('block', models.BooleanField(default=False)),
                ('publish_time', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='articles', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
