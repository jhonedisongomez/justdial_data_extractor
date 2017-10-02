# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawler_manager', '0004_auto_20171002_0335'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='crawelissue',
            name='created_by',
        ),
    ]
