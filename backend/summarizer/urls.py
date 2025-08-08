from django.urls import path
from . import views

urlpatterns = [
    path('summarize/', views.summarize_article, name='summarize_article'),
    path('health/', views.health_check, name='health_check'),
] 