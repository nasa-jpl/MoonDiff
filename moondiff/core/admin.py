from django.contrib import admin
from moondiff.core.models import *

admin.site.site_header = "MoonDiff admin"
admin.site.site_title = "MoonDiff admin"

admin.site.register(SpacecraftCamera)
admin.site.register(Image)
admin.site.register(PairSet)
admin.site.register(Pair)
admin.site.register(Annotation)
admin.site.register(AnnotationReview)

# Register your models here.
