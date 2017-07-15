import argparse
import csv
import logging

from django.core.management.base import BaseCommand
from django.db import transaction

from quips.quips.models import Quip, Quote, Speaker

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Imports a CSV file containing quips data'

    def add_arguments(self, parser):
        parser.add_argument('file', help='csv containing quips', type=argparse.FileType('r'))
        parser.add_argument('--purge', help='purges all quip data, resetting to a clean state', action='store_true')

    def handle(self, *args, **options):
        if options['purge']:
            quotes = Quote.objects.all()
            self.stdout.write(self.style.WARNING('Deleting all {} Quotes'.format(quotes.count())))
            quotes.delete()

            quips = Quip.objects.all()
            self.stdout.write(self.style.WARNING('Deleting all {} Quips'.format(quips.count())))
            quips.delete()

            speakers = Speaker.objects.all()
            self.stdout.write(self.style.WARNING('Deleting all {} Speakers'.format(speakers.count())))
            speakers.delete()

        f = options['file']
        row_num = 0
        successes = 0
        with f:
            header_row = csv.Sniffer().has_header(f.read(1024))
            f.seek(0)
            reader = csv.reader(f)
            for row in reader:
                try:
                    if header_row:
                        header_row = False
                        continue
                    with transaction.atomic():
                        self._import_quip_row(row)
                    successes += 1
                except Exception as e:
                    self.stderr.write(self.style.ERROR('Failed to import row {}: {}'.format(row_num, e)))
                row_num += 1
            self.stdout.write(self.style.SUCCESS('Successfully imported {} quips'.format(successes)))

    def _import_quip_row(self, row):
        """
        Import a row (at this point effectively a tuple) of quip data.

        Each row should have data with columns in this order:

            date, context, quote, speaker

        Additional quotes and speakers may repeat in pairs after the first.
        """

        date, context = row[0].decode('utf-8'), row[1].decode('utf-8')
        quip = Quip(date=date, context=context)
        quip.save()

        quote_pairs = (pair for pair in zip(row[2::2], row[3::2]) if pair[0])
        for quote_text, speaker_name in quote_pairs:
            speaker, created = Speaker.objects.get_or_create(name=speaker_name.decode('utf-8'))
            # if created:
            #     self.stdout.write(self.style.WARNING(
            #         'Speaker "{}" did not exist and has been created'.format(speaker_name)))
            quote = Quote(text=quote_text.decode('utf-8'), speaker=speaker, quip=quip)
            quote.save()
