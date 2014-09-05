# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='assignee',
            field=models.ForeignKey(verbose_name='assigné à', null=True, blank=True, to=settings.AUTH_USER_MODEL, related_name='assigned_to'),
        ),
        migrations.AlterField(
            model_name='issue',
            name='state',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Relevé'), (0, 'Annulé'), (2, 'Confirmé'), (3, 'À faire'), (4, 'À tester'), (5, 'Testé'), (6, 'Terminé')], verbose_name='statut', default=1),
        ),
    ]
