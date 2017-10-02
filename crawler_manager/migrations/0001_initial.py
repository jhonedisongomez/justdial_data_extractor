# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CrawelIssue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword', models.CharField(max_length=100)),
                ('city_name', models.CharField(max_length=100)),
                ('instance_index', models.IntegerField()),
                ('title', models.CharField(max_length=100, default='')),
                ('rating', models.CharField(max_length=100, default='')),
                ('votes', models.CharField(max_length=100, default='')),
                ('contact', models.CharField(max_length=100, default='')),
                ('address', models.CharField(max_length=100, default='')),
                ('website', models.CharField(max_length=100, default='')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, default='')),
            ],
        ),
    ]
