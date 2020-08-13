from django.contrib import admin
from .models import Student,institution,Watch,Community,joinkey,User,day
from import_export import resources
from import_export.admin import ExportActionModelAdmin, ImportExportMixin, ImportMixin, ExportMixin
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter   # pip install django-admin-rangefilter, installed app ='rangefilter',
from import_export.widgets import ForeignKeyWidget
from import_export import resources, fields,widgets
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import Group

class institutionResource(resources.ModelResource):

 
    class Meta:
        model = institution
        exclude = ('id',)
        import_id_fields = ('institution_number',)


class UserResource(resources.ModelResource):
    class Meta:
        model = User
        fields = ('username','first_name', 'email')
        exclude = ('id',)
        import_id_fields = ('username',)
    
    def before_save_instance(self, instance, using_transactions, dry_run):
        instance.username=str(instance.username)

    def after_save_instance(self,instance, using_transactions, dry_run):
        u = User.objects.get(username=instance.username)
        u.set_password(u.username)
        u.save()
        Watch_Student = Student(user=u)
        Watch_Student.save()
        for a in institution.objects.all():
            w = Watch(Watch_Student=Watch_Student, Watch_institution=a)
            w.save()

class myUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','first_name','is_active', 'is_staff','groups')
                                       

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class myUserCreationForm2(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','first_name', 'is_active', 'is_staff')



class UserAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = UserResource
    list_display=['username','first_name', 'email']
    change_form = myUserCreationForm2
    add_form = myUserCreationForm
    search_fields = ['username',]
    list_filter = ('is_staff',)
    def get_form(self, request, obj=None, **kwargs):
        if not obj:
            self.form = self.add_form
        else:
            self.form = self.change_form

        return super(UserAdmin, self).get_form(request, obj, **kwargs)
    class Meta:
        model = User
        exclude = ('id',)
        import_id_fields = ('username',)



class StudentResource(resources.ModelResource):
     
     user = fields.Field(
        column_name='user', attribute='user',
        widget=ForeignKeyWidget(User, 'username')
    )



                    

     class Meta:
        model = Student
        exclude = ('id',)
        import_id_fields = ('user',)






class StudentAdmin(ExportMixin, admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    resource_class=StudentResource
    list_display = ['get_id','name' ,'CompleteState','feeling']
    search_fields = ['created', 'user__username']
    list_filter = ('CompleteState',)
    def name(self,obj):
        return obj.user.first_name
    def get_id(self,obj):
        return obj.user.username



class myUserCreationForm_institutution(forms.ModelForm):
    class Meta:
        model = institution
        fields = ('quiz1','quiz2', 'quiz3', 'qrcode','latitude','longitude','gps_error')

class institutionAdmin( admin.ModelAdmin):
    change_form = myUserCreationForm_institutution
    def get_form(self, request, obj=None, **kwargs):
        if not obj:
            self.form = self.add_form
        else:
            self.form = self.change_form

        return super(institutionAdmin, self).get_form(request, obj, **kwargs)
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    list_display = ['institution_number', 'quiz1','quiz2','quiz3']
    resource_class=institutionResource
    pass

class watchAdmin(ExportMixin,admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def get_username(sef,obj):
        return obj.Watch_Student.user.username

    list_display = ['get_username','Watch_institution', 'quiz_answer','stampStatus']
    search_fields = ['Watch_Student__user__username','Watch_institution__institution_number', 'modify_date']
    list_filter =(('modify_date',DateRangeFilter),) # pip install django-admin-rangefilter, installed app ='rangefilter',
    pass

class CommunityAdmin(ExportMixin,admin.ModelAdmin):
    def has_add_permission(self, request):
        return False
    list_display = ['created','author','text']
    search_fields = ['author','id','text']
    pass

class joinkeyAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    pass

#class TotalAdmin(ImportExportMixin, admin.ModelAdmin):
#   list_display = ['day','counts',]
#   pass



class dayAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    list_display = ['number','Mon','Tue' ,'Wed','Thu','Fri','Sat','Sun']
   
    def number(self,obj):
        D1=0
        D2=0
        D3=0
        D4=0
        D5=0
        D6=0
        D7=0
        x=Watch.objects.all()
        for a in x:
            d=str(a.create_Stamp_date)
            if d[0:3]=='Mon':
                D1+=1
            elif d[0:3]=='Tue':
                D2+=1
            elif d[0:3]=='Wed':
                D3+=1
            elif d[0:3]=='Thu':
                D4+=1
            elif d[0:3]=='Fri':
                D5+=1
            elif d[0:3]=='Sat':
                D6+=1
            elif d[0:3]=='Sun':
                D7+=1
        obj.Mon=D1
        obj.Tue=D2
        obj.Wed=D3
        obj.Thu=D4
        obj.Fri=D5
        obj.Sat=D6
        obj.Sun=D7
        return '횟수'




# Register your models here.
admin.site.register(Student,StudentAdmin)
admin.site.register(institution,institutionAdmin)
admin.site.register(Watch,watchAdmin)
admin.site.register(Community,CommunityAdmin)
#admin.site.register(Total,TotalAdmin)
admin.site.register(joinkey,joinkeyAdmin)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(day, dayAdmin)
admin.site.unregister(Group)

