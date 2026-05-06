from rest_framework.views import APIView
from ..serializers.journal_with_lines import JournalWithLinesInputSerializer
from ..services.journal_with_lines import JournalWithLinesService


class JournalWithLinesCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = JournalWithLinesInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        return JournalWithLinesService.create(data)


class JournalWithLinesReviseAPIView(APIView):
    def post(self, request, journal_id):
        serializer = JournalWithLinesInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_data = serializer.validated_data

        return JournalWithLinesService.revise(journal_id, new_data)


class JournalWithLinesRetrieveAPIView(APIView):
    def get(self, request, journal_id):
        return JournalWithLinesService.get(journal_id)


class JournalWithLinesListAPIView(APIView):
    def get(self, request):
        return JournalWithLinesService.list()


class JournalWithLinesHistoryAPIView(APIView):
    def get(self, request, journal_id, *args, **kwargs):
        return JournalWithLinesService.history(str(journal_id))

        # if not history_journals:
        #     return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        # # 既存の出力用Serializerをそのまま使い回す
        # serializer = JournalOutputSerializer(history_journals, many=True)
        # return Response(serializer.data, status=status.HTTP_200_OK)
