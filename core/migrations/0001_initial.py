# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Prediction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('zodiac', models.CharField(max_length=100)),
                ('prediction', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sex', models.BooleanField(default=False)),
                ('mobile', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('user', models.OneToOneField(related_name='userprofiletoUser', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Zodiac',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(unique=True)),
                ('zodiac', models.ManyToManyField(related_name='zodiactoprediction', to='core.Prediction')),
            ],
        ),
    ]
