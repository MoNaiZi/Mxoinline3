# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-06-16 08:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_course_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='category',
            field=models.CharField(default='后端开发', max_length=20, verbose_name='课程类别'),
        ),
    ]