# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20151013_1416'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='dob',
            field=models.DateField(default=datetime.datetime(2015, 10, 13, 9, 13, 5, 919534, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
