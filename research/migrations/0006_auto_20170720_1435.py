# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('research', '0005_auto_20160804_1022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='researchstudy',
            name='research_nurse',
            field=models.ManyToManyField(related_name='research_nurse_user', verbose_name='Research Practitioner', to=settings.AUTH_USER_MODEL),
        ),
    ]
