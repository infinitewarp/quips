import csv
import io

import faker
from django.test import TestCase

from .. import models
from ..management.commands.importquips import Command as ImportQuipsCommand

FAKER = faker.Faker()


class ImportQuipsTest(TestCase):
    """Management command 'importquips' test case."""

    def test_handle_one_bad_csv_row_aborts_everything(self):
        """Assert handle aborts and rollbacks everything if only one row is bad."""
        good_row = [FAKER.date(), FAKER.sentence(), FAKER.sentence(), FAKER.name()]
        bad_row = FAKER.words()

        with io.StringIO() as the_file:
            csv_writer = csv.writer(the_file, delimiter=",")
            csv_writer.writerow(good_row)
            csv_writer.writerow(bad_row)
            the_file.seek(0)

            with io.StringIO() as stdout, io.StringIO() as stderr:
                options = {"purge": False, "file": the_file}
                ImportQuipsCommand(stdout=stdout, stderr=stderr).handle(**options)
                stderr.seek(0)
                stderr_str = stderr.read()
                self.assertIn("Failed to import row", stderr_str)
                self.assertIn("Rolling back", stderr_str)

        self.assertEqual(models.Speaker.objects.all().count(), 0)
        self.assertEqual(models.Quote.objects.all().count(), 0)
        self.assertEqual(models.Quip.objects.all().count(), 0)

    def test_import_quip_row_with_new_speakers(self):
        """Assert _import_quip_row creates new speakers."""
        quip_date = FAKER.date()
        quip_context = FAKER.sentence()
        first_name = FAKER.name()
        first_quote = FAKER.sentence()
        second_name = FAKER.name()
        second_quote = FAKER.sentence()
        row = [
            quip_date,
            quip_context,
            first_quote,
            first_name,
            second_quote,
            second_name,
        ]

        ImportQuipsCommand()._import_quip_row(row)

        speakers = models.Speaker.objects.all()
        self.assertEqual(len(speakers), 2)
        self.assertEqual(speakers[0].name, first_name)
        self.assertEqual(speakers[1].name, second_name)

        quotes = models.Quote.objects.all()
        self.assertEqual(len(quotes), 2)
        self.assertEqual(quotes[0].text, first_quote)
        self.assertEqual(quotes[0].speaker, speakers[0])
        self.assertEqual(quotes[1].text, second_quote)
        self.assertEqual(quotes[1].speaker, speakers[1])

        quip = models.Quip.objects.get()
        self.assertEqual(quip.context, quip_context)
        quip_quotes = quip.quotes.all()
        self.assertEqual(quip_quotes[0], quotes[0])
        self.assertEqual(quip_quotes[1], quotes[1])

    def test_import_quip_row_with_existing_speaker(self):
        """Assert _import_quip_row reuses an existing speaker."""
        quip_date = FAKER.date()
        quip_context = FAKER.sentence()
        first_name = FAKER.name()
        first_quote = FAKER.sentence()
        second_name = FAKER.name()
        second_quote = FAKER.sentence()
        row = [
            quip_date,
            quip_context,
            first_quote,
            first_name,
            second_quote,
            second_name,
        ]

        models.Speaker.objects.create(name=first_name)

        ImportQuipsCommand()._import_quip_row(row)

        speakers = models.Speaker.objects.all()
        self.assertEqual(len(speakers), 2)
        self.assertEqual(speakers[0].name, first_name)
        self.assertEqual(speakers[1].name, second_name)

        quotes = models.Quote.objects.all()
        self.assertEqual(len(quotes), 2)
        self.assertEqual(quotes[0].speaker, speakers[0])
        self.assertEqual(quotes[1].speaker, speakers[1])

        quip = models.Quip.objects.get()
        self.assertEqual(quip.context, quip_context)
        self.assertEqual(quip.quotes.all().count(), 2)

    def test_import_quip_row_strips_whitespace(self):
        """Assert _import_quip_row strips whitespace around values."""
        quip_date = FAKER.date()
        quip_context = FAKER.sentence()
        first_name = FAKER.name()
        first_quote = FAKER.sentence()
        row = [
            f" {quip_date} ",
            f" {quip_context} ",
            f" {first_quote} ",
            f" {first_name} ",
        ]

        models.Speaker.objects.create(name=first_name)

        ImportQuipsCommand()._import_quip_row(row)

        speaker = models.Speaker.objects.get()
        self.assertEqual(speaker.name, first_name)

        quote = models.Quote.objects.get()
        self.assertEqual(quote.text, first_quote)

        quip = models.Quip.objects.get()
        self.assertEqual(quip.context, quip_context)
