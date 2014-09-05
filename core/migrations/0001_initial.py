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
            name='Issue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('type', models.PositiveSmallIntegerField(verbose_name='type', default=1, choices=[(1, 'Bug'), (2, 'Amélioration'), (3, 'Nouvelle fonctionnalité')])),
                ('state', models.PositiveSmallIntegerField(verbose_name='statut', default=1, choices=[(1, 'Relevé'), (0, 'Annulé'), (2, 'Confirmé'), (3, 'À faire'), (4, 'À tester'), (5, 'Testé'), (6, 'En production')])),
                ('priority', models.PositiveSmallIntegerField(verbose_name='priorité', default=3, choices=[(1, 'Un jour...'), (2, 'Faible'), (3, 'Normale'), (4, 'Haute'), (5, 'Critique'), (6, 'Bloquant')])),
                ('title', models.CharField(verbose_name='titre', max_length=100)),
                ('description', models.TextField(verbose_name='description')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='créé le')),
                ('updated_on', models.DateTimeField(auto_now=True, verbose_name='mis à jour le')),
                ('assignee', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='assigné à', related_name='assigned_to')),
                ('reporter', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='relevé par', related_name='reported')),
            ],
            options={
                'verbose_name': 'tâche',
                'verbose_name_plural': 'tâches',
            },
            bases=(models.Model,),
        ),
    ]
