from django.urls import path
from .views import UploadCSVView, DatasetListView, DatasetDetailView, SummaryView, ReportDownloadView

urlpatterns = [
    path('upload/', UploadCSVView.as_view(), name='upload'),
    path('datasets/', DatasetListView.as_view(), name='datasets'),
    path('datasets/<int:pk>/', DatasetDetailView.as_view(), name='dataset-detail'),
    path('datasets/<int:pk>/summary/', SummaryView.as_view(), name='dataset-summary'),
    path('datasets/<int:pk>/report/', ReportDownloadView.as_view(), name='dataset-report'),
]
