# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-07 09:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testcase',
            name='testcase',
            field=models.IntegerField(),
        ),
        migrations.AlterUniqueTogether(
            name='testcase',
            unique_together=set([('problem_id', 'testcase')]),
        ),
    ]
