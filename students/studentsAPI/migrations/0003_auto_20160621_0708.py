# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-21 07:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('studentsAPI', '0002_auto_20160621_0706'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256, verbose_name='Назва')),
                ('notes', models.TextField(blank=True, verbose_name='Нотатки')),
                ('leader', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='studentsAPI.Student', verbose_name='Староста')),
            ],
        ),
        migrations.AddField(
            model_name='student',
            name='student_group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='studentsAPI.Group', verbose_name='Група'),
        ),
    ]