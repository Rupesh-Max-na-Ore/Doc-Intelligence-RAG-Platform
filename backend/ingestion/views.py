from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ingestion.services.book_ingestion_service import ingest_books


class IngestBooksView(APIView):
    def post(self, request):
        # 🔹 Input validation
        try:
            limit = int(request.data.get("limit", 10))
        except (ValueError, TypeError):
            return Response(
                {
                    "status": "error",
                    "message": "Invalid 'limit' value. Must be an integer."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            results = ingest_books(limit=limit)

            return Response(
                {
                    "status": "success",
                    "data": results
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {
                    "status": "error",
                    "message": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )