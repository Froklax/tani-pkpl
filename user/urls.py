from django.urls import path
from user.views import register, show_success, user_login, user_logout

app_name = 'user'

urlpatterns = [
    path('register/', register, name="register"),
    path('', show_success, name="success"),
    path('login/', user_login, name="login"),
    path('logout/', user_logout, name='logout'),
]