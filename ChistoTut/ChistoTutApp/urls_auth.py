from django.urls import path
from django.contrib.auth.views import LogoutView

from ChistoTutApp.views.auth_views import CustomLoginView, RegisterView
from ChistoTutApp.views.dashboard_views import MainView

app_name = 'auth'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
