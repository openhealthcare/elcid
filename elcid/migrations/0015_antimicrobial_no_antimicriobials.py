# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elcid', '0014_consultant_consultantatdischarge'),
    ]

    operations = [
        migrations.AddField(
            model_name='antimicrobial',
            name='no_antimicriobials',
            field=models.NullBooleanField(default=False),
        ),
    ]
