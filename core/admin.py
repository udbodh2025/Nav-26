from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import (
    MenuItem, Module, Form, Task, Project, Transaction,
    Unit, Level, Bank, Currency, Designation, StaffDetails
)
from django.contrib.admin import TabularInline

# Existing admin classes (MenuItemAdmin, ModuleAdmin, FormAdmin, TaskAdmin, ProjectAdmin, TransactionAdmin) remain unchanged
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'parent', 'order')
    list_filter = ('parent', 'groups')
    search_fields = ('name', 'url')
    filter_horizontal = ('groups',)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "groups":
            kwargs["queryset"] = Group.objects.all()
        return super().formfield_for_manytomany(db_field, request, **kwargs)

class ModuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'menu_item')
    filter_horizontal = ('users',)

class FormAdmin(admin.ModelAdmin):
    list_display = ('name', 'module')

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'assigned_to', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'project', 'assigned_to')
    search_fields = ('title', 'description')
    raw_id_fields = ('assigned_to', 'created_by')
    
class TaskInline(TabularInline):
    model = Task
    extra = 1

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'module', 'created_at', 'updated_at')
    list_filter = ('module',)
    search_fields = ('name', 'description')
    inlines = [TaskInline]

admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(Module, ModuleAdmin)
admin.site.register(Form, FormAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Project, ProjectAdmin)

class UnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')

class LevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')

class BankAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'swift_code')
    search_fields = ('name', 'code', 'swift_code')

class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'symbol')
    search_fields = ('name', 'code')

class DesignationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class StaffDetailsInline(admin.StackedInline):
    model = StaffDetails
    can_delete = False
    verbose_name_plural = 'Staff Details'

class UserAdmin(BaseUserAdmin):
    inlines = (StaffDetailsInline,)

# Unregister the original User admin
admin.site.unregister(User)

# Register the new User admin
admin.site.register(User, UserAdmin)

# Register the new models
admin.site.register(Unit, UnitAdmin)
admin.site.register(Level, LevelAdmin)
admin.site.register(Bank, BankAdmin)
admin.site.register(Currency, CurrencyAdmin)
admin.site.register(Designation, DesignationAdmin)

# Existing model registrations remain unchanged

