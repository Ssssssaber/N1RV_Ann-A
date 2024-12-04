from django.urls import path, include
from . import views

app_name = 'auth'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', views.RegisterView.as_view(), name='registration')
]