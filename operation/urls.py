from django.urls import path
from . import views

urlpatterns = [
    path('', views.OperationList.as_view()),
]