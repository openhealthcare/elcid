# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elcid', '0012_haem_info_patient_types'),
    ]

    operations = [
        migrations.AddField(
            model_name='haeminformation',
            name='type_of_transplant_fk',
            field=models.ForeignKey(blank=True, to='elcid.HaemTransplantType', null=True),
        ),
        migrations.AddField(
            model_name='haeminformation',
            name='type_of_transplant_ft',
            field=models.CharField(default=b'', max_length=255, null=True, blank=True),
        ),
    ]
