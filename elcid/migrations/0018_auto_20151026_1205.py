# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elcid', '0017_merge'),
    ]

    operations = [
        migrations.RenameField(
            model_name='antimicrobial',
            old_name='no_antimicriobials',
            new_name='no_antimicrobials',
        ),
    ]
