from django.contrib import admin
from .models import Breakout

@admin.register(Breakout)
class BreakoutAdmin(admin.ModelAdmin):
    list_display = ('currency_pair', 'breakout_time', 'alert_sent')
    list_filter = ('currency_pair', 'alert_sent')
    search_fields = ('currency_pair',)
    