from rest_framework.views import APIView
from journal.serializers.journal_with_lines import (
    JournalWithLinesInputSerializer,
    JournalWithLinesOutputSerializer,
)
from journal.services.journal_with_lines import JournalWithLinesService
from rest_framework.response import Response
from rest_framework import status


class JournalWithLinesCreateAPIView(APIView):
    def post(self, request):
        input = JournalWithLinesInputSerializer(data=request.data)
        input.is_valid(raise_exception=True)

        journal = JournalWithLinesService.create(input.validated_data)

        output = JournalWithLinesOutputSerializer(journal)
        return Response(output.data, status=status.HTTP_201_CREATED)


class JournalWithLinesReviseAPIView(APIView):
    def post(self, request, journal_id):
        input = JournalWithLinesInputSerializer(data=request.data)
        input.is_valid(raise_exception=True)

        journal = JournalWithLinesService.revise(journal_id, input.validated_data)

        output = JournalWithLinesOutputSerializer(journal)
        return Response(output.data, status=status.HTTP_201_CREATED)


class JournalWithLinesListAPIView(APIView):
    def get(self, request):
        journals = JournalWithLinesService.list()

        output = JournalWithLinesOutputSerializer(journals, many=True)

        return Response(output.data, status=status.HTTP_200_OK)


class JournalWithLinesHistoryAPIView(APIView):
    def get(self, request, journal_id):
        journals = JournalWithLinesService.history(journal_id)

        output = JournalWithLinesOutputSerializer(journals, many=True)

        return Response(output.data, status=status.HTTP_200_OK)

        # if not history_journals:
        #     return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        # # 既存の出力用Serializerをそのまま使い回す
        # serializer = JournalOutputSerializer(history_journals, many=True)
        # return Response(serializer.data, status=status.HTTP_200_OK)
