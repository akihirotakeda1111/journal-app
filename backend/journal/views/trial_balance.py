from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..services.trial_balance import TrialBalanceService


class TrialBalanceAPIView(APIView):
    def get(self, request, *args, **kwargs):
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        data = TrialBalanceService.get(start_date, end_date)
        return Response(data, status=status.HTTP_200_OK)
