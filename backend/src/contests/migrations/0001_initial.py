# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-07 09:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('problems', '0001_initial'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('contest_code', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(unique=True)),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('start_contest', models.DateTimeField()),
                ('end_contest', models.DateTimeField()),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='creator', to='accounts.Profile')),
            ],
            options={
                'ordering': ['-creation_date'],
            },
        ),
        migrations.CreateModel(
            name='ContestsHaveProblems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.IntegerField(default=0)),
                ('contest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contests.Contest')),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='problems.Problem')),
            ],
            options={
                'verbose_name': 'Contest Problem',
            },
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.IntegerField(default=0)),
                ('contest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contests.Contest')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participant', to='accounts.Profile')),
            ],
        ),
        migrations.AddField(
            model_name='contest',
            name='participants',
            field=models.ManyToManyField(through='contests.Participant', to='accounts.Profile'),
        ),
        migrations.AddField(
            model_name='contest',
            name='problems',
            field=models.ManyToManyField(through='contests.ContestsHaveProblems', to='problems.Problem'),
        ),
    ]
