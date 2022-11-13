from django.urls import path
from . import views

urlpatterns = [
    path('', views.RepositoryList.as_view()),
    path('<str:name>/', views.RepositoryDetail.as_view()),
]