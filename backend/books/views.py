from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer


class BookListView(APIView):
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)