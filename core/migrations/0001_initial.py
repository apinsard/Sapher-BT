# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Check',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('message', models.CharField(max_length=255, blank=True, verbose_name='message')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('content', models.TextField(help_text='The text will be formatted in <a target=_blank href="http://en.wikipedia.org/wiki/Markdown">Mardown</a>. HTML also supported for advanced formatting. A line break behaves the same as a space. Two consecutive line breaks mark a new paragraph.', verbose_name='comment')),
                ('posted_on', models.DateTimeField(auto_now_add=True, verbose_name='posted on')),
                ('edited_on', models.DateTimeField(null=True, auto_now=True, verbose_name='edited on')),
                ('author', models.ForeignKey(related_name='comments', verbose_name='author', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'comments',
                'verbose_name': 'comment',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('description', models.TextField(help_text='The text will be formatted in <a target=_blank href="http://en.wikipedia.org/wiki/Markdown">Mardown</a>. HTML also supported for advanced formatting. A line break behaves the same as a space. Two consecutive line breaks mark a new paragraph.', verbose_name='description')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='created on')),
                ('updated_on', models.DateTimeField(null=True, auto_now=True, verbose_name='updated on')),
                ('assignee', models.ForeignKey(related_name='assigned_to', null=True, to=settings.AUTH_USER_MODEL, verbose_name='assignee', blank=True)),
            ],
            options={
                'ordering': ['-priority', 'state'],
                'verbose_name_plural': 'issues',
                'verbose_name': 'issue',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='IssuePriority',
            fields=[
                ('id', models.PositiveSmallIntegerField(serialize=False, help_text='This ID will be used by `UserSettings.priority_filters` as 2^(ID).', validators=[django.core.validators.MaxValueValidator(31)], verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name='name', unique=True)),
                ('icon', models.CharField(max_length=50, help_text='See http://getbootstrap.com/components/#glyphicons', default='asterisk', verbose_name='glyphicon')),
                ('level', models.PositiveSmallIntegerField(help_text='The higher number, the higher priority.', default=100, verbose_name='level')),
            ],
            options={
                'ordering': ['-level'],
                'verbose_name_plural': 'priority levels',
                'verbose_name': 'priority level',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='IssueState',
            fields=[
                ('id', models.PositiveSmallIntegerField(serialize=False, help_text='This ID will be used by `UserSettings.state_filters` as 2^(ID).', validators=[django.core.validators.MaxValueValidator(31)], verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name='name', unique=True)),
                ('css_class', models.CharField(max_length=50, help_text='Predefined styles are "default" (gray), "primary" (blue), "success" (green), "info" (cyan), "warning" (orange) and "danger" (red). You can also create your own in your stylesheet.', default='default', verbose_name='CSS class (progress-bar-)')),
                ('progression', models.PositiveSmallIntegerField(help_text='Between 0 and 100.', default=100, verbose_name='progression', validators=[django.core.validators.MaxValueValidator(100)])),
            ],
            options={
                'ordering': ['progression', 'id'],
                'verbose_name_plural': 'states of progress',
                'verbose_name': 'state of progress',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='IssueType',
            fields=[
                ('id', models.PositiveSmallIntegerField(serialize=False, help_text='This ID will be used by `UserSettings.type_filters` as 2^(ID).', validators=[django.core.validators.MaxValueValidator(31)], verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name='name', unique=True)),
                ('css_class', models.CharField(max_length=50, help_text='Predefined styles are "default" (gray), "primary" (blue), "success" (green), "info" (cyan), "warning" (orange) and "danger" (red). You can also create your own in your stylesheet.', default='default', verbose_name='CSS class (label-)')),
                ('icon', models.CharField(max_length=50, help_text='See http://getbootstrap.com/components/#glyphicons', default='asterisk', verbose_name='glyphicon')),
            ],
            options={
                'ordering': ['id'],
                'verbose_name_plural': 'types',
                'verbose_name': 'type',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.CharField(max_length=3, validators=[django.core.validators.RegexValidator('^[A-Z]{2,}$')], primary_key=True, serialize=False, help_text='Two or three uppercase letters to quickly identify this project', verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name', unique=True)),
            ],
            options={
                'verbose_name_plural': 'projects',
                'verbose_name': 'project',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserSettings',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('type_filters', models.PositiveIntegerField(default=2147483647, verbose_name='type filters')),
                ('state_filters', models.PositiveIntegerField(default=2147483647, verbose_name='state filters')),
                ('priority_filters', models.PositiveIntegerField(default=2147483647, verbose_name='priority filters')),
                ('orderby', models.CharField(max_length=100, default='-priority__level', choices=[('-priority__level', 'Descending priority level'), ('priority__level', 'Ascending priority level'), ('-state__progression', 'Descending state progression'), ('state__progression', 'Ascending state progression')], verbose_name='sort by')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='issue',
            name='priority',
            field=models.ForeignKey(to='core.IssuePriority', verbose_name='priority', default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='issue',
            name='project',
            field=models.ForeignKey(to='core.Project', verbose_name='project', default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='issue',
            name='reporter',
            field=models.ForeignKey(related_name='reported', verbose_name='reporter', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='issue',
            name='state',
            field=models.ForeignKey(to='core.IssueState', verbose_name='state', default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='issue',
            name='type',
            field=models.ForeignKey(to='core.IssueType', verbose_name='type', default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='issue',
            field=models.ForeignKey(related_name='comments', verbose_name='issue', to='core.Issue'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='check',
            name='comment',
            field=models.ForeignKey(related_name='checks', null=True, to='core.Comment', verbose_name='comment', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='check',
            name='issue',
            field=models.ForeignKey(related_name='checks+', verbose_name='issue', to='core.Issue'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='check',
            name='requested',
            field=models.ForeignKey(related_name='checks_received', verbose_name='recipient', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='check',
            name='requester',
            field=models.ForeignKey(related_name='checks_sent', verbose_name='sender', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
