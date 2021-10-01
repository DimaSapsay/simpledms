from django.urls import path, re_path
from documents import views


urlpatterns = [
    path('', views.DocumentList.as_view()),
    path('<int:pk>/', views.DocumentDetail.as_view()),
    re_path(r'^period/(?P<start>\d{4}-\d{2}-\d{2})/(?P<end>\d{4}-\d{2}-\d{2})/$',
            views.DocumentPeriodList.as_view()),
    path('archive/', views.ArchiveList.as_view()),
    path('archive/<int:pk>/', views.ArchiveDetail.as_view()),
]
