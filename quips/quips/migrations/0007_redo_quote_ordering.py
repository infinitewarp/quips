from django.db import migrations


def copy_old_quote_order(apps, schema_editor):
    """Copy the old-style order data for Quotes to the new field."""
    Quote = apps.get_model("quips", "Quote")

    class OldStyleOrderedQuote(Quote):
        class Meta:
            proxy = True
            app_label = "quips"

        managed = False

    ordered_quotes = OldStyleOrderedQuote.objects.filter(old_order__gt=0)
    for quote in ordered_quotes:
        quote._order = quote.old_order
        quote.save()


class Migration(migrations.Migration):

    dependencies = [
        ("quips", "0006_speaker_should_obfuscate"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="quote",
            options={},
        ),
        migrations.RenameField(
            model_name="quote",
            old_name="order",
            new_name="old_order",
        ),
        migrations.AlterOrderWithRespectTo(
            name="quote",
            order_with_respect_to="quip",
        ),
        migrations.RunPython(copy_old_quote_order),
    ]
