from django.urls import path
from .views.account import AccountListAPIView

urlpatterns = [
    path("management/account/list/", AccountListAPIView.as_view()),
]
