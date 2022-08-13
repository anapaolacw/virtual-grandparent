from django.contrib import admin

from .models import Help, Helper, OldPerson, HelpCandidates

# Register your models here.
admin.site.register(Help)
admin.site.register(Helper)
admin.site.register(OldPerson)
admin.site.register(HelpCandidates)
