from django.contrib import admin
from journal.models import Journal, JournalLine
from management.models import Account

admin.site.register(Journal)
admin.site.register(JournalLine)
admin.site.register(Account)
