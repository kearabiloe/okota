# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('okota', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderTimeSlot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.TimeField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='order',
            name='time_slot',
            field=models.ForeignKey(blank=True, to='okota.OrderTimeSlot', null=True),
            preserve_default=True,
        ),
    ]
