from django.contrib import admin
from .models import *

class VideoAdmin(admin.ModelAdmin):
    list_display = ("title", "creator", "upload_date", "is_public")

admin.site.register(Video, VideoAdmin)
admin.site.register(Comment)
admin.site.register(CreatorProfile)
admin.site.register(Like)
admin.site.register(Channel)
admin.site.register(Subscribe)
