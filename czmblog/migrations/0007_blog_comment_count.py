# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('czmblog', '0006_remove_blog_comment_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='comment_count',
            field=models.IntegerField(default=2),
            preserve_default=False,
        ),
    ]
