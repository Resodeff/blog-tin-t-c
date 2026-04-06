from django.contrib import admin
from .models import CATEGORY, TAG, POST, COMMENT

admin.site.register(CATEGORY)
admin.site.register(TAG)
admin.site.register(POST)
admin.site.register(COMMENT)
