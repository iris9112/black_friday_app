from django.shortcuts import render_to_response
from django.views.generic.base import TemplateView
from django.conf import settings

from .models import Document
from .utils import previewDataFrame



# Create your views here.

class index(TemplateView):
    template_name = "app/index.html"


class BlankView(TemplateView):
    template_name = "app/blank.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        documents = Document.objects.all()
        context["documents"] = documents
        # esto seria más util como un detail view
        context['preview'] = previewDataFrame()
        print(type(previewDataFrame()))

        return context

class ChartsView(TemplateView):
    template_name = "app/charts.html"


class TablesView(TemplateView):
    template_name = "app/tables.html"