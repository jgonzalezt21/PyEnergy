from django.urls import path

from .views import IndexView, RegisterFormView, RegisterYearArchiveView, RegisterArchiveIndexView, \
    RegisterMonthArchiveView, RegisterDayArchiveView, RegisterUpdateView, ReportProvinceTemplateView, \
    ReportLocalsTemplateView, ReportRegisterDayListView, ajax_local

app_name = 'energy'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('register/list/', RegisterArchiveIndexView.as_view(), name='register_archive'),
    path('register/<int:year>/', RegisterYearArchiveView.as_view(), name='register_year'),
    path('register/<int:year>/<int:month>/', RegisterMonthArchiveView.as_view(), name='register_month'),
    path('register/<int:year>/<int:month>/<int:day>/', RegisterDayArchiveView.as_view(), name='register_day'),
    path('register/add/', RegisterFormView.as_view(), name='add'),
    path('register/edit/<int:pk>/', RegisterUpdateView.as_view(), name='edit'),

    # Reports
    path('register/reports/province/<int:year>/', ReportProvinceTemplateView.as_view(),
         name='register_report_province'),
    path('register/reports/local/<int:year>/', ReportLocalsTemplateView.as_view(),
         name='register_report_local'),
    path('register/reports/all/<int:year>/<int:month>/', ReportRegisterDayListView.as_view(),
         name='register_report_day'),

    # Ajax
    path('register/ajax/local/', ajax_local, name='ajax_local'),
]
