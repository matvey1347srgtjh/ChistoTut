from django.urls import path, include

urlpatterns = [
    path('', include('ChistoTutApp.urls_dashboard')),
    path('auth/', include('ChistoTutApp.urls_auth')),
]
