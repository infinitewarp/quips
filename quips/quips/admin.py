# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin

from quips.quips.models import Quip, Quote, Speaker


class QuoteAdmin(OrderedModelAdmin):
    list_display = ('id', 'quip', 'text', 'speaker', 'move_up_down_links')


admin.site.register(Quote, QuoteAdmin)
admin.site.register(Quip)
admin.site.register(Speaker)
