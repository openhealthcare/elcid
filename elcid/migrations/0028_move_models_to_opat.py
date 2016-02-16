# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

model_names = [
    "OPATLineAssessment", "Opat_rvt", "OPATOutstandingIssues",
    "OPATReview", "OPATMeta", "OPATOutcome", "OPATRejection",
    "Unplanned_stop"
]

class Migration(migrations.Migration):
    dependencies = [
        ('opat', '0002_opatdressingtype'),
        ('elcid', '0027_ridrtistudydiagnosis'),
    ]

    database_operations = [
        migrations.AlterModelTable(i, "opat_%s" % i.lower()) for i in model_names
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=database_operations
            )
    ]
