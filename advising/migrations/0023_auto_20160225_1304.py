# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-25 18:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advising', '0022_remove_student_statuses'),
    ]

    operations = [
        migrations.AlterField(
            model_name='status',
            name='order',
            field=models.IntegerField(null=True),
        ),
    ]