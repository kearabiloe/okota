# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('okota', '0002_auto_20150224_1000'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ordertimeslot',
            old_name='time',
            new_name='end_time',
        ),
        migrations.AddField(
            model_name='ordertimeslot',
            name='start_time',
            field=models.TimeField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
