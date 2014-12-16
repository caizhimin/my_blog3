# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('czmblog', '0004_auto_20141118_2315'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tag',
            options={'ordering': ['-tag_count']},
        ),
        migrations.AddField(
            model_name='blog',
            name='comment_count',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
