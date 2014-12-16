# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('czmblog', '0002_auto_20141117_1702'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='tag_count',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
    ]
