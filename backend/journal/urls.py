from django.urls import path
from journal.views.journal_with_lines import (
    JournalWithLinesCreateAPIView,
    JournalWithLinesCancelAPIView,
    JournalWithLinesReviseAPIView,
    JournalWithLinesListAPIView,
    JournalWithLinesHistoryAPIView,
)
from .views.trial_balance import TrialBalanceAPIView

urlpatterns = [
    path("journal/", JournalWithLinesCreateAPIView.as_view()),
    path("journal/cancel/<uuid:journal_id>/", JournalWithLinesCancelAPIView.as_view()),
    path("journal/revise/<uuid:journal_id>/", JournalWithLinesReviseAPIView.as_view()),
    path("journal/list/", JournalWithLinesListAPIView.as_view()),
    path(
        "journal/<uuid:journal_id>/history/", JournalWithLinesHistoryAPIView.as_view()
    ),
    path("journal/trial_balance/", TrialBalanceAPIView.as_view()),
]
