from django.urls import path
from . import views

urlpatterns = [
    path('me', views.ListMe.as_view()),
    path('search', views.ListSearch.as_view()),
    path('employee', views.ListEmployees.as_view()),
    path('employee/<int:model_id>', views.ListEmployee.as_view()),
]
