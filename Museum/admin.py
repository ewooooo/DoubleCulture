from django.contrib import admin
from .models import Student,institution,Watch,Community,Total
from import_export.admin import ExportActionModelAdmin, ImportExportMixin, ImportMixin
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter   # pip install django-admin-rangefilter, installed app ='rangefilter',

class StudentAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['user', 'CompleteState','created','modify_date']
    search_fields = ['created', 'user__username']
    list_filter = ('CompleteState',)
    pass

class institutionAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['institution_number', 'quiz']

    pass

class watchAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['Watch_Student','Watch_institution', 'quiz_answer']
    search_fields = ['Watch_Student__user__username','Watch_institution__institution_number', 'modify_date']
    list_filter =(('modify_date',DateRangeFilter),) # pip install django-admin-rangefilter, installed app ='rangefilter',
    pass

class CommunityAdmin(ImportExportMixin, admin.ModelAdmin):
    search_fields = ['author__user__username','id']
    pass

class TotalAdmin(ImportExportMixin, admin.ModelAdmin):

    pass




# Register your models here.
admin.site.register(Student,StudentAdmin)
admin.site.register(institution,institutionAdmin)
admin.site.register(Watch,watchAdmin)
admin.site.register(Community,CommunityAdmin)
admin.site.register(Total,TotalAdmin)