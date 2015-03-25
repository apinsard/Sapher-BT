# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='check',
            name='is_unread',
            field=models.BooleanField(verbose_name='unread', default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='check',
            name='requested_on',
            field=models.DateTimeField(verbose_name='date', default=datetime.datetime(2015, 3, 25, 10, 56, 41, 164624), auto_now_add=True),
            preserve_default=False,
        ),
    ]
