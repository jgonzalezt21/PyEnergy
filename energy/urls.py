from django.urls import path

from .views import IndexView, RegisterFormView, RegisterYearArchiveView, RegisterArchiveIndexView, \
    RegisterMonthArchiveView, RegisterDayArchiveView, RegisterUpdateView

app_name = 'energy'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('register/list/', RegisterArchiveIndexView.as_view(), name='register_archive'),
    path('register/<int:year>/', RegisterYearArchiveView.as_view(), name='register_year'),
    path('register/<int:year>/<int:month>/', RegisterMonthArchiveView.as_view(), name='register_month'),
    path('register/<int:year>/<int:month>/<int:day>/', RegisterDayArchiveView.as_view(), name='register_day'),
    path('register/add/', RegisterFormView.as_view(), name='add'),
    path('register/edit/<int:pk>/', RegisterUpdateView.as_view(), name='edit'),
]
