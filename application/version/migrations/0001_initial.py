# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=500, null=True, blank=True)),
                ('location', models.TextField(max_length=1000, null=True, blank=True)),
                ('created', models.DateTimeField(auto_now=True)),
                ('editable', models.DateTimeField(null=True, blank=True)),
                ('slug', models.SlugField(blank=True)),
            ],
        ),
    ]
