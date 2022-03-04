from django.contrib import admin, messages
from django.utils.translation import ngettext
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
    list_per_page = 16


@admin.register(Register)
class RegisterAdmin(admin.ModelAdmin):
    list_display = ['is_edit', 'reading_day', 'local', 'reading', 'plan', 'real', 'diff']
    list_filter = ['is_edit', 'reading_day', 'local']
    date_hierarchy = 'reading_day'
    actions = ['register_is_edit']
    list_per_page = 31

    @admin.action(description='Cerrar Captación')
    def register_is_edit(self, request, queryset):
        updated = queryset.update(is_edit=False)
        self.message_user(request, ngettext(
            'cerrada la captación de %d registro.',
            'cerrada la captación de %d registros.',
            updated,
        ) % updated, messages.SUCCESS)
