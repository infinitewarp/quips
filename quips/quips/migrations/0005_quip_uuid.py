# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-18 23:08
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("quips", "0004_clique_20170901_0223"),
    ]

    operations = [
        migrations.AlterField(
            model_name="quip",
            name="uuid",
            field=models.UUIDField(
                default=uuid.uuid4, editable=False, unique=True, verbose_name="UUID"
            ),
        ),
    ]
