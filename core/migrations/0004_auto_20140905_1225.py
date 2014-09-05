# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0003_auto_20140904_1150'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSettings',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('filters', models.PositiveIntegerField(default=65015, verbose_name='filtres')),
                ('orderby', models.CharField(choices=[('-priority', 'Priorité décroissante'), ('priority', 'Priorité croissante'), ('-state', 'État décroissant'), ('state', 'État croissant')], max_length=20, default='-priority', verbose_name='trier par')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='issue',
            options={'ordering': ['-priority', 'state'], 'verbose_name_plural': 'tâches', 'verbose_name': 'tâche'},
        ),
    ]
