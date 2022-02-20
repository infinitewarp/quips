# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid as uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from slugify import slugify


class Clique(models.Model):
    """Clique is a grouping of Speakers."""

    name = models.CharField(_("Name of Clique"), blank=False, max_length=255)
    slug = models.SlugField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Clique, self).save(*args, **kwargs)

    def get_speakers(self):
        speakers = Speaker.objects.filter(cliques__in=[self.id]).order_by("id")
        return speakers


class Speaker(models.Model):
    """Speaker is the person who said the Quote."""

    name = models.CharField(_("Name of Speaker"), blank=False, max_length=255)
    cliques = models.ManyToManyField(Clique)
    should_obfuscate = models.BooleanField(
        _("Should the displayed name be obfuscated"), default=True
    )

    def __str__(self):
        return self.name


class Quip(models.Model):
    """Quip is the exchange of one or more Quotes with optional context."""

    uuid = models.UUIDField(_("UUID"), unique=True, default=uuid.uuid4, editable=False)
    context = models.CharField(_("Context of the Quote"), blank=True, max_length=255)
    date = models.DateField(_("Date of the Quote"), null=False)

    def __str__(self):
        return "{}: {} {}".format(self.id, self.date, self.context)


class Quote(models.Model):
    """Quote is what a Speaker said as part of a Quip."""

    text = models.CharField(_("Text of the Quote"), blank=False, max_length=512)
    quip = models.ForeignKey(Quip, related_name="quotes", on_delete=models.CASCADE)
    speaker = models.ForeignKey(Speaker, on_delete=models.CASCADE)

    class Meta:
        order_with_respect_to = "quip"

    @property
    def is_slash_me(self):
        return self.text[0:4] == "/me "

    def __str__(self):
        if self.is_slash_me:
            return self.text[4:]
        return self.text
