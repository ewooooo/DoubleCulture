from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import  Museum,StudentProject,Watch
from import_export.admin import ExportActionModelAdmin, ImportExportMixin, ImportMixin

class MuseumAdmin(ImportExportMixin, admin.ModelAdmin):
    pass

class StudentProjectAdmin(ImportExportMixin, admin.ModelAdmin):
    pass

class WatchAdmin(ImportExportMixin, admin.ModelAdmin):
    pass


# Register your models here.
admin.site.register(Museum,MuseumAdmin)
admin.site.register(StudentProject,StudentProjectAdmin)
admin.site.register(Watch,WatchAdmin)
