from django.contrib import admin
from .models import SlackAskUs,Log,AuthenticatedSpaces
# Register your models here.
admin.site.register(SlackAskUs)
admin.site.register(Log)
admin.site.register(AuthenticatedSpaces)