# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('czmblog', '0003_tag_tag_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='tag_count',
            field=models.IntegerField(),
        ),
    ]
