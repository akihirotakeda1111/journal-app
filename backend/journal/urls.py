from django.urls import path
from journal.views.journal_with_lines import (
    JournalWithLinesCreateAPIView,
    JournalWithLinesCancelAPIView,
    JournalWithLinesReviseAPIView,
    JournalWithLinesListAPIView,
    JournalWithLinesHistoryAPIView,
)
from journal.views.trial_balance import TrialBalanceAPIView
from journal.views.evidence_upload import EvidenceUploadAPIView
from journal.views.evidence_download import EvidenceDownloadAPIView
from journal.views.evidence import (
    JournalEvidenceCreateAPIView,
    JournalEvidenceListAPIView,
)

urlpatterns = [
    path("journal/", JournalWithLinesCreateAPIView.as_view()),
    path("journal/cancel/<uuid:journal_id>/", JournalWithLinesCancelAPIView.as_view()),
    path("journal/revise/<uuid:journal_id>/", JournalWithLinesReviseAPIView.as_view()),
    path("journal/list/", JournalWithLinesListAPIView.as_view()),
    path(
        "journal/<uuid:journal_id>/history/", JournalWithLinesHistoryAPIView.as_view()
    ),
    path("journal/trial_balance/", TrialBalanceAPIView.as_view()),
    path("journal/evidence/upload/", EvidenceUploadAPIView.as_view()),
    path(
        "journal/evidence/download/<int:evidence_id>/",
        EvidenceDownloadAPIView.as_view(),
    ),
    path("journal/evidence/<uuid:journal_id>/", JournalEvidenceCreateAPIView.as_view()),
    path(
        "journal/evidence/list/<uuid:journal_id>/", JournalEvidenceListAPIView.as_view()
    ),
]
