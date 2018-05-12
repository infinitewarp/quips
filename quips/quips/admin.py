# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin

from quips.quips.models import Clique, Quip, Quote, Speaker


class QuoteInline(admin.TabularInline):
    model = Quote
    extra = 1


class QuoteAdmin(OrderedModelAdmin):
    list_display = ('id', 'quip', 'text', 'speaker', 'move_up_down_links')
    list_filter = ('speaker__cliques__name', 'speaker__name',)


class QuipAdmin(admin.ModelAdmin):
    inlines = [QuoteInline]
    readonly_fields = ['uuid']


class SpeakerAdmin(admin.ModelAdmin):
    list_filter = ('cliques__name',)


admin.site.register(Quote, QuoteAdmin)
admin.site.register(Quip, QuipAdmin)
admin.site.register(Speaker, SpeakerAdmin)
admin.site.register(Clique)
