from django.urls import path

from .views import BlankView, ChartsView, TablesView, PredictionView
from . import views


urlpatterns = [
    path('', BlankView.as_view(), name='blank'),
    path('predic', views.PredictionView, name='prediction'),
    path('charts', ChartsView.as_view(), name='charts'),
    path('tables', TablesView.as_view(), name='tables'),
]