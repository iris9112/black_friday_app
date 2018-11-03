from django.urls import path

from .views import index, BlankView, ChartsView, TablesView, PredictionView
from . import views


urlpatterns = [
    path('', index.as_view(), name='index'),
    path('predic', views.PredictionView, name='prediction'),
    path('blank', BlankView.as_view(), name='blank'),
    path('charts', ChartsView.as_view(), name='charts'),
    path('tables', TablesView.as_view(), name='tables'),
]