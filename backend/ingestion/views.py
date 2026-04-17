from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ingestion.services.book_ingestion_service import ingest_books


class IngestBooksView(APIView):
    def post(self, request):
        limit = request.data.get("limit", 10)

        try:
            results = ingest_books(limit=limit)

            return Response({
                "status": "success",
                "ingested_count": len(results),
                "books": results
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "status": "error",
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)