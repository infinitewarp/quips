# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from ordered_model.admin import OrderedModelAdmin

from quips.quips.models import Clique, Quip, Quote, Speaker


class QuoteInline(admin.TabularInline):
    model = Quote
    extra = 1


class QuoteAdmin(OrderedModelAdmin):
    list_display = ('id', 'quip', 'text', 'speaker', 'move_up_down_links')
    list_filter = ('speaker__cliques__name', 'speaker__name',)
    fields = ('text', 'quip', 'speaker', 'quip_link')
    readonly_fields = ['quip_link']

    def quip_link(self, obj):
        href = reverse('quips:detail', args=(obj.quip.uuid,))
        return format_html(f'<a href="{href}">{obj.quip.uuid}</a>')
    quip_link.short_description = 'Quip UUID'


class QuipAdmin(admin.ModelAdmin):
    inlines = [QuoteInline]
    fields = ('context', 'date', 'link')
    readonly_fields = ['link']

    def link(self, obj):
        href = reverse('quips:detail', args=(obj.uuid,))
        return format_html(f'<a href="{href}">{obj.uuid}</a>')
    link.short_description = 'UUID'


class SpeakerAdmin(admin.ModelAdmin):
    list_filter = ('cliques__name',)


admin.site.register(Quote, QuoteAdmin)
admin.site.register(Quip, QuipAdmin)
admin.site.register(Speaker, SpeakerAdmin)
admin.site.register(Clique)
