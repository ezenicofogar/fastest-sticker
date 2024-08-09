from django.contrib import admin
from . import models
# Register your models here.

class ImageContentAdmin(admin.ModelAdmin):
    model = models.ImageContent
    fields = ['image',]
class QueryGroupAdmin(admin.ModelAdmin):
    model = models.QueryGroup
    fields = ['type', 'printed']
    list_display = ['pk', 'printed', 'type']
class QueryImageRelationAdmin(admin.ModelAdmin):
    model = models.QueryImageRelation
    fields = ['querygroup', 'imagecontent']
    list_display = ['querygroup', 'imagecontent']
    ordering = ('querygroup', 'imagecontent')

admin.site.register(models.ImageContent, ImageContentAdmin)
admin.site.register(models.QueryGroup, QueryGroupAdmin)
admin.site.register(models.QueryImageRelation, QueryImageRelationAdmin)