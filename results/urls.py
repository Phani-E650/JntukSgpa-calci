from django.urls import path
from results import views
urlpatterns = [
    path('', views.get_results, name='get_results'),
]