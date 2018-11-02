from django.shortcuts import render_to_response
from django.views.generic.base import TemplateView
from django.conf import settings

from .models import Document
from .utils import previewDataFrame, prediction

# https://www.hackerearth.com/practice/notes/bokeh-interactive-visualization-library-use-graph-with-django-template/

# Create your views here.

class index(TemplateView):
    template_name = "app/index.html"


class BlankView(TemplateView):
    template_name = "app/blank.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # trabajamos siempre sobre el ultimo dataset
        document = Document.objects.all().last()
        context["document"] = document

        # esto seria más util como un detail view
        context['preview'] = previewDataFrame(document)

        return context


class ChartsView(TemplateView):
    template_name = "app/charts.html"


class TablesView(TemplateView):
    template_name = "app/tables.html"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #
    #     # trabajamos siempre sobre el ultimo dataset
    #     document = Document.objects.all().last()
    #     # esto seria más util como un detail view
    #     context['prediction'] = prediction(document)
    #
    #     return context
