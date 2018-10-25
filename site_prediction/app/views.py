from django.shortcuts import render_to_response
from django.views.generic.base import TemplateView

# Create your views here.

class index(TemplateView):
    template_name = "app/index.html"


class BlankView(TemplateView):
    template_name = "app/blank.html"


class ChartsView(TemplateView):
    template_name = "app/charts.html"


class TablesView(TemplateView):
    template_name = "app/tables.html"