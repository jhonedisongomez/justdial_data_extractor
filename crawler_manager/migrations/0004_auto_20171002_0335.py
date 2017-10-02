# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('crawler_manager', '0003_auto_20171002_0325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crawelissue',
            name='created_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True, related_name='CrawelIssues'),
        ),
    ]
