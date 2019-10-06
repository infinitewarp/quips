import argparse
import csv
import logging

from django.core.management.base import BaseCommand
from django.db import transaction

from quips.quips.models import Quip, Quote, Speaker

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Imports a CSV file containing quips data"

    def add_arguments(self, parser):
        parser.add_argument(
            "file", help="csv containing quips", type=argparse.FileType("r")
        )
        parser.add_argument(
            "--purge",
            help="purges all quip data, resetting to a clean state",
            action="store_true",
        )

    def handle(self, *args, **options):
        try:
            with transaction.atomic():
                if options.get("purge", False):
                    self._do_purge()

                the_file = options["file"]
                with the_file:
                    self._handle_file(the_file)
        except Exception as e:
            self.stderr.write(
                self.style.WARNING("Rolling back! {}: {}".format(e.__class__, e))
            )

    def _do_purge(self):
        """Purge all quip data."""
        quotes = Quote.objects.all()
        self.stdout.write(
            self.style.WARNING("Deleting all {} Quotes".format(quotes.count()))
        )
        quotes.delete()

        quips = Quip.objects.all()
        self.stdout.write(
            self.style.WARNING("Deleting all {} Quips".format(quips.count()))
        )
        quips.delete()

        speakers = Speaker.objects.all()
        self.stdout.write(
            self.style.WARNING("Deleting all {} Speakers".format(speakers.count()))
        )
        speakers.delete()

    def _handle_file(self, the_file):
        """Read the CSV and import its contents."""
        successes = 0
        for row_num, row in enumerate(csv.reader(the_file)):
            try:
                self._import_quip_row(row)
                successes += 1
            except Exception as e:
                self.stderr.write(
                    self.style.ERROR("Failed to import row {}: {}".format(row_num, e))
                )
                raise e
        self.stdout.write(
            self.style.SUCCESS("Successfully imported {} quips".format(successes))
        )

    def _import_quip_row(self, row):
        """
        Import a row (at this point effectively a tuple) of quip data.

        Each row should have data with columns in this order:

            date, context, quote, speaker

        Additional quotes and speakers may repeat in pairs after the first.
        """
        date, context = row[0].strip(), row[1].strip()
        quip = Quip(date=date, context=context)
        quip.save()

        quote_pairs = (pair for pair in zip(row[2::2], row[3::2]) if pair[0])
        quotes = list()
        for quote_text, speaker_name in quote_pairs:
            quote_text = quote_text.strip()
            speaker_name = speaker_name.strip()
            speaker, created = Speaker.objects.get_or_create(name=speaker_name)
            if created:
                self.stdout.write(
                    self.style.WARNING(
                        'Speaker "{}" did not exist and has been created'.format(
                            speaker_name
                        )
                    )
                )
            quote = Quote(text=quote_text, speaker=speaker, quip=quip)
            quote.save()
            quotes.append(quote)

        if len(quotes) > 1:
            quote_order = [quote.id for quote in quotes]
            quip.set_quote_order(quote_order)
