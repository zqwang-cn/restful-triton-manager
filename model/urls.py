from django.urls import path
from . import views

urlpatterns = [
    path('', views.ModelList.as_view()),
    path('<str:name>/', views.ModelDetail.as_view()),
    path('<str:name>/inputs/', views.InputList.as_view()),
    path('<str:name>/inputs/<str:input_name>/', views.InputDetail.as_view()),
    path('<str:name>/outputs/', views.OutputList.as_view()),
    path('<str:name>/outputs/<str:output_name>/', views.OutputDetail.as_view()),
    path('<str:name>/versions/', views.VersionList.as_view()),
    path('<str:name>/versions/<int:version>/', views.VersionDetail.as_view()),
    path('<str:name>/versions/<int:version>/custom-files/', views.CustomFileList.as_view()),
    path('<str:name>/versions/<int:version>/custom-files/<int:id>/', views.CustomFileDetail.as_view()),
]