# Generated by Django 2.1.4 on 2019-01-21 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("quips", "0008_drop_old_quote_order_field"),
    ]

    operations = [
        migrations.AlterField(
            model_name="quote",
            name="text",
            field=models.CharField(max_length=512, verbose_name="Text of the Quote"),
        ),
    ]
