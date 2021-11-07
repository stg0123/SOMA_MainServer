from django.contrib import admin
from .models import *

admin.site.register(ST_User)
admin.site.register(Presentation)
admin.site.register(KeyWord)
admin.site.register(Script)
admin.site.register(PresentationFile)
admin.site.register(PresentationResult)
admin.site.register(Knowhow)