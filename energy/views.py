import json
import calendar
from datetime import date, timedelta, datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.serializers.json import DjangoJSONEncoder
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum
from django.db.models.functions import ExtractMonth
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView, FormView
from django.views.generic.dates import ArchiveIndexView, YearArchiveView, MonthArchiveView, DayArchiveView
from .forms import RegisterUpdateForm, PlanningCreateForm
from .models import Local, Register


# Create your views here.
class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'energy/index.html'

    def get(self, *args, **kwargs):
        # En caso q el user no tien local, redirect to the admin site
        try:
            if not locals_user(my_user(self)):
                return redirect('/admin/')
        except ObjectDoesNotExist:
            return redirect('/admin/')
        return super(IndexView, self).get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        today = date.today()
        month = int(today.strftime('%m'))

        user = my_user(self)
        local_user = locals_user(user)
        qs = Register.objects.filter(reading_day__month=month, local__in=local_user). \
            values('reading_day').annotate(plan=Sum('plan'), real=Sum('real')).order_by('reading_day')
        context['data_local'] = json.dumps(list(qs), cls=DjangoJSONEncoder)

        if user.is_staff:
            year = int(today.strftime('%Y'))
            province = province_user(user)
            qs = Register.objects.filter(reading_day__year=year, local__province=province). \
                annotate(month=ExtractMonth('reading_day')).values('month'). \
                annotate(plan2=Sum('plan'), real2=Sum('real')).values('month', 'plan2', 'real2')
            context['data_prov'] = json.dumps(list(qs), cls=DjangoJSONEncoder)
            context['province'] = province
            context['year'] = year

        context['local'] = local_user
        context['month'] = today
        context['title'] = 'Principal'
        return context


class RegisterArchiveIndexView(LoginRequiredMixin, ArchiveIndexView):
    model = Register
    allow_future = True
    date_field = 'reading_day'
    extra_context = {'title': 'Seleccione año'}

    def get_date_list(self, queryset, date_type=None, ordering='ASC'):
        return super().get_date_list(queryset.filter(local__in=locals_user(my_user(self))))


class RegisterYearArchiveView(LoginRequiredMixin, YearArchiveView):
    queryset = Register.objects.all()
    allow_future = True
    date_field = 'reading_day'
    extra_context = {'title': 'Seleccione mes'}

    def get_date_list(self, queryset, date_type=None, ordering='ASC'):
        return super().get_date_list(queryset.filter(local__in=locals_user(my_user(self))))


class RegisterMonthArchiveView(LoginRequiredMixin, MonthArchiveView):
    queryset = Register.objects.all()
    allow_future = True
    month_format = '%m'
    date_field = 'reading_day'
    extra_context = {'title': 'Seleccione día'}

    def get_date_list(self, queryset, date_type=None, ordering='ASC'):
        return super().get_date_list(queryset.filter(local__in=locals_user(my_user(self))))


class RegisterDayArchiveView(LoginRequiredMixin, DayArchiveView):
    allow_future = True
    month_format = '%m'
    date_field = 'reading_day'
    extra_context = {'title': 'Registro del día'}

    def get_queryset(self):
        return Register.objects.filter(local__in=locals_user(my_user(self)))


class RegisterFormView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    form_class = PlanningCreateForm
    success_url = reverse_lazy('energy:add')
    success_message = 'Planificasión del mes creada.'
    extra_context = {'title': 'Nuevo Registro'}
    template_name = 'energy/register_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['local'] = all_locals_prov_user(my_user(self))
        return kwargs

    def form_valid(self, form):
        reading_day = form.data['reading_day']
        local = Local.objects.get(pk=form.data['local'])
        plan_lv = form.data['plan_lv']
        plan_sd = form.data['plan_sd']

        day_one = datetime.strptime(reading_day, '%Y-%m-%d').replace(day=1)
        weekday, days_month = calendar.monthrange(day_one.year, day_one.month)

        for i in range(days_month):
            reading_day = day_one + timedelta(days=i)
            # WEEKDAY 0-Lunes, 1-Martes......5-Sabado, 6-Domingo
            if reading_day.weekday() in [5, 6]:
                plan = plan_sd
            else:
                plan = plan_lv
            Register.objects.create(reading_day=reading_day, plan=plan, local=local)

        return super().form_valid(form)


class RegisterUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Register
    form_class = RegisterUpdateForm
    success_message = 'Registro del día actualizado.'
    extra_context = {'title': 'Actualizar Registro'}

    def form_valid(self, form):
        yesterday = form.instance.reading_day - timedelta(days=1)
        try:
            yesterday_reading = Register.objects.get(reading_day=yesterday, local=form.instance.local).reading
        except ObjectDoesNotExist:
            yesterday_reading = 0
        form.instance.real = form.instance.reading - yesterday_reading
        return super().form_valid(form)

    def get_success_url(self):
        today = self.object.reading_day
        year = today.year
        month = today.month
        day = today.day
        return reverse_lazy('energy:register_day', kwargs={'year': year, 'month': month, 'day': day})


def my_user(self):
    return self.request.user


def locals_user(user):
    return Local.objects.filter(user=user)


def province_user(user):
    return locals_user(user)[0].province


def all_locals_prov_user(user):
    return Local.objects.filter(province=province_user(user))
