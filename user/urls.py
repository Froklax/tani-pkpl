from django.urls import path
from user.views import register, show_success

urlpatterns = [
    path('', register, name="register"),
    path("success/", show_success, name="success"),
]