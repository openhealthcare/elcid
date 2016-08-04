# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('research', '0004_migrate_content_types'),
    ]

    operations = [
        migrations.AlterField(
            model_name='researchstudy',
            name='clinical_lead',
            field=models.ManyToManyField(related_name='clinical_lead_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='researchstudy',
            name='research_nurse',
            field=models.ManyToManyField(related_name='research_nurse_user', verbose_name=b'Research Practitioner', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='researchstudy',
            name='researcher',
            field=models.ManyToManyField(related_name='researcher_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='researchstudy',
            name='scientist',
            field=models.ManyToManyField(related_name='scientist_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
