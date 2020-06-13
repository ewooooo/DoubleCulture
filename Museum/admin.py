from django.contrib import admin
from .models import Student, institution, Watch, Community, Total, joinkey, User
from import_export import resources
from import_export.admin import ExportActionModelAdmin, ImportExportMixin, ImportMixin, ImportExportActionModelAdmin
from rangefilter.filter import DateRangeFilter, \
    DateTimeRangeFilter  # pip install django-admin-rangefilter, installed app ='rangefilter',
from import_export.widgets import ForeignKeyWidget
from import_export import resources, fields
from django.contrib.auth.forms import UserCreationForm
from django import forms


class institutionResource(resources.ModelResource):
    class Meta:
        model = institution
        exclude = ('id',)
        import_id_fields = ('institution_number',)


class UserResource(resources.ModelResource):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        exclude = ('id',)
        import_id_fields = ('username',)

    def before_save_instance(self, instance, using_transactions, dry_run):
        instance.username = str(instance.username)

    def after_save_instance(self, instance, using_transactions, dry_run):
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
        fields = ('username', 'first_name', 'last_name', 'is_active', 'is_staff', 'groups')

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
        fields = ('username', 'first_name', 'last_name', 'is_active', 'is_staff')


class UserAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = UserResource
    list_display = ['username', 'first_name', 'last_name', 'email']
    change_form = myUserCreationForm2
    add_form = myUserCreationForm

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


class StudentAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = StudentResource
    list_display = ['user', 'CompleteState', 'created', 'modify_date']
    search_fields = ['created', 'user__username']
    list_filter = ('CompleteState',)
    pass


class institutionAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['institution_number', 'quiz1', 'quiz2', 'quiz3']
    resource_class = institutionResource
    pass


class watchAdmin(ImportExportMixin, admin.ModelAdmin):
    def get_username(sef, obj):
        return obj.Watch_Student.user.username

    list_display = ['get_username', 'Watch_institution', 'quiz_answer', 'stampStatus']
    search_fields = ['Watch_Student__user__username', 'Watch_institution__institution_number', 'modify_date']
    list_filter = (
    ('modify_date', DateRangeFilter),)  # pip install django-admin-rangefilter, installed app ='rangefilter',
    pass


class CommunityAdmin(ImportExportMixin, admin.ModelAdmin):
    search_fields = ['author__user__username', 'id']
    pass


class joinkeyAdmin(ImportExportMixin, admin.ModelAdmin):
    pass


class TotalAdmin(ImportExportMixin, admin.ModelAdmin):
    pass


# Register your models here.
admin.site.register(Student, StudentAdmin)
admin.site.register(institution, institutionAdmin)
admin.site.register(Watch, watchAdmin)
admin.site.register(Community, CommunityAdmin)
admin.site.register(Total, TotalAdmin)
admin.site.register(joinkey, joinkeyAdmin)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)