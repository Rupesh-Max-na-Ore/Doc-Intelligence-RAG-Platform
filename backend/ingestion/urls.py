from django.urls import path
from .views import IngestBooksView

urlpatterns = [
    path('ingest/', IngestBooksView.as_view(), name='ingest-books'),
]