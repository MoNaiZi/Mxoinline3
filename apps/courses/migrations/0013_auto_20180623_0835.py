# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-06-23 08:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0012_auto_20180623_0747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='image',
            field=models.FileField(blank=True, default='', null=True, upload_to='teacher/%Y/%m', verbose_name='视频'),
        ),
    ]
