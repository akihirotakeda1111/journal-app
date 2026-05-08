from django.urls import path
from management.views.account import AccountListAPIView

urlpatterns = [
    path("management/account/list/", AccountListAPIView.as_view()),
]
