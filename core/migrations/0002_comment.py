# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('content', models.TextField(verbose_name='commentaire')),
                ('posted_on', models.DateTimeField(verbose_name='posté le', auto_now_add=True)),
                ('edited_on', models.DateTimeField(auto_now=True, verbose_name='modifié le')),
                ('author', models.ForeignKey(related_name='comments', verbose_name='auteur', to=settings.AUTH_USER_MODEL)),
                ('issue', models.ForeignKey(related_name='comments', verbose_name='tâche', to='core.Issue')),
            ],
            options={
                'verbose_name': 'commentaire',
                'verbose_name_plural': 'commentaires',
            },
            bases=(models.Model,),
        ),
    ]
