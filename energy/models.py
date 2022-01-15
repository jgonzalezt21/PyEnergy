from django.contrib import admin
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Province(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name=_('Nombre'))

    class Meta:
        verbose_name = _('Provincia')
        verbose_name_plural = _('Provincias')

    def __str__(self):
        return self.name

    @admin.display(
        description=_('Cant. Locales')
    )
    def count_locals(self) -> int:
        return Local.objects.filter(province=self.pk).count()


class Local(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name=_('Nombre'))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('Usuario'))
    province = models.ForeignKey(Province, on_delete=models.CASCADE, verbose_name=_('Provincia'))

    class Meta:
        verbose_name = _('Local')
        verbose_name_plural = _('Locales')

    def __str__(self):
        return self.name


class Register(models.Model):
    reading_day = models.DateField(verbose_name=_('Fecha'))
    plan = models.PositiveIntegerField(verbose_name=_('Plan'))
    real = models.PositiveIntegerField(default=0, verbose_name=_('Real'))
    reading = models.PositiveIntegerField(default=0, verbose_name=_('Lectura'))
    local = models.ForeignKey(Local, on_delete=models.CASCADE, verbose_name=_('Local'))

    @property
    def diff(self) -> int:
        return self.plan - self.real

    class Meta:
        verbose_name = _('Registro')
        verbose_name_plural = _('Registros')

    def __str__(self):
        return '%s %s' % (self.local.name, self.reading_day)
