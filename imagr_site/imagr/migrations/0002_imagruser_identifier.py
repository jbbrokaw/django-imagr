# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imagr', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagruser',
            name='identifier',
            field=models.CharField(default='', unique=True, max_length=40),
            preserve_default=False,
        ),
    ]
