from django.contrib import admin

from energy.models import Province, Local, Register


# Register your models here.
@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ['name', 'count_locals']


@admin.register(Local)
class LocalAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'province']
    search_fields = ['name']
    list_filter = ['user', 'province']
    list_per_page = 15


@admin.register(Register)
class RegisterAdmin(admin.ModelAdmin):
    list_display = ['reading_day', 'local', 'reading', 'plan', 'real', 'diff']
    list_filter = ['reading_day', 'local']
    date_hierarchy = 'reading_day'
    list_per_page = 30
