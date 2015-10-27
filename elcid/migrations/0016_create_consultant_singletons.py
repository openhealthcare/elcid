# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def create(apps, schema_editor):
    Episode = apps.get_model("opal", "Episode")
    ConsultantAtDischarge = apps.get_model("elcid", "ConsultantAtDischarge")
    episodes = Episode.objects.all()
    consultants = [ConsultantAtDischarge(episode=episode) for episode in episodes]
    ConsultantAtDischarge.objects.bulk_create(consultants)

def remove(apps, schema_editor):
    ConsultantAtDischarge = apps.get_model("elcid", "ConsultantAtDischarge")
    ConsultantAtDischarge.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('elcid', '0015_antimicrobial_no_antimicriobials'),
    ]

    operations = [
        migrations.RunPython(create, reverse_code=remove)
    ]
