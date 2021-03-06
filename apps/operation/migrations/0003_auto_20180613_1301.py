# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-06-13 13:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0002_coursecomments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfavorite',
            name='fav_id',
            field=models.IntegerField(default=0, verbose_name='数据id'),
        ),
        migrations.AlterField(
            model_name='userfavorite',
            name='fav_type',
            field=models.IntegerField(choices=[(1, '课程'), (2, '课程机构'), (3, '讲师')]),
        ),
    ]
