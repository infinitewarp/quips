from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("quips", "0007_redo_quote_ordering"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="quote",
            name="old_order",
        ),
    ]
