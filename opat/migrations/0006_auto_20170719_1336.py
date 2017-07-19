# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def migrate_forwards(apps, schema_editor):
    Episode = apps.get_model("opal", "Episode")
    for e in Episode.objects.all():
        rejection = e.opatrejection_set.first()

        if rejection:
            e.start = rejection.date
            e.end = rejection.date
            e.save()
        else:
            referral = e.tagging_set.filter(
                value="opat_referrals", archived=False
            ).exists()

            if referral:
                e.start = None
                e.end = None
                e.save()


def migrate_backwards(app, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('opat', '0005_auto_20170321_1325'),
        ('opal', '0031_auto_20170719_1018')
    ]

    operations = [
        migrations.RunPython(
            migrate_forwards, reverse_code=migrate_backwards
        ),
    ]
