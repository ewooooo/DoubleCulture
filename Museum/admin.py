from django.contrib import admin
from .models import StudentProject,Museum,Watch,Total
from import_export.admin import ExportActionModelAdmin, ImportExportMixin, ImportMixin
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter   # pip install django-admin-rangefilter, installed app ='rangefilter',

class StudentProjectAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['user', 'CompleteStatue','created','modify_date']
    search_fields = ['created', 'user__username']
    list_filter = ('CompleteStatue',) 
    pass

class MuseumAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['museum_number', 'howtogo', 'quiz1','quiz2', 'quiz3']

    pass

class watchAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['project','museum', 'quiz1_answer', 'quiz2_answer','quiz3_answer']
    search_fields = ['project__user__username','museum__museum_number', 'create_date', 'modify_date']
    list_filter =( ('create_date',DateRangeFilter),('modify_date',DateRangeFilter))# pip install django-admin-rangefilter, installed app ='rangefilter',
    pass

class TotalAdmin(ImportExportMixin, admin.ModelAdmin):

    pass




# Register your models here.
admin.site.register(StudentProject,StudentProjectAdmin)
admin.site.register(Museum,MuseumAdmin)
admin.site.register(Watch,watchAdmin)
admin.site.register(Total,TotalAdmin)

