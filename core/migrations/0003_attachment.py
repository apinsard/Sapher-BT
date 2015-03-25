# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20150325_1056'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('type', models.CharField(verbose_name='type', choices=[('rev', 'commit'), ('file', 'file')], max_length=30)),
                ('url', models.URLField(verbose_name='url')),
                ('name', models.CharField(verbose_name='name', max_length=100)),
                ('description', models.TextField(verbose_name='description')),
                ('issue', models.ForeignKey(verbose_name='issue', related_name='attachments', to='core.Issue')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
