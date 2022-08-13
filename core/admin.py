from django.contrib import admin

from .models import Help, Helper, OldPerson

# Register your models here.
admin.site.register(Help)
admin.site.register(Helper)
admin.site.register(OldPerson)

