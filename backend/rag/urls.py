# backend/rag/urls.py

from django.urls import path
from .views import QueryBooksView

urlpatterns = [
    path('query/', QueryBooksView.as_view(), name='rag-query'),
]