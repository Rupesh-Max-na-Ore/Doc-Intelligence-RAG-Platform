from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rag.services.rag_service import answer_query


class QueryBooksView(APIView):
    def post(self, request):
        query = request.data.get("query")

        if not query:
            return Response(
                {"error": "Query is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        result = answer_query(query)

        return Response(result, status=status.HTTP_200_OK)