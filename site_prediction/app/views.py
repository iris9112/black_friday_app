from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from django.views.generic.base import TemplateView
from django.conf import settings

from .models import Document
from .utils import (previewDataFrame, prediction, read_csv, units_per_product,
                   top_sales, top_user)

# Create your views here.

class BlankView(TemplateView):
    template_name = "app/blank.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # trabajamos siempre sobre el ultimo dataset
        document = Document.objects.all().last()
        context["document"] = document

        # TODO: esto seria más util como un detail view
        context['preview'] = previewDataFrame(document)

        return context


class ChartsView(TemplateView):
    template_name = "app/charts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        df = read_csv('solution.csv')

        # marital status
        df_marital = df['Marital_Status'].value_counts()
        context['marital_0'] = df_marital[0]
        context['marital_1'] = df_marital[1]

        # gender
        df_gender = df['Gender'].value_counts()
        context['M'] = df_gender[0]
        context['F'] = df_gender[1]

        # age
        age = df['Age'].value_counts()
        values = list(age)
        # [53604, 26739, 24452, 11188, 9463, 5294, 3655]
        # [2, 3, 1, 4, 5, 6, 0]
        context['data_age'] = values

        return context

class TablesView(TemplateView):
    template_name = "app/tables.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        df = read_csv('solution.csv')
        context['preview'] = df.head().to_html(classes="table table-bordered", index=False)
        context['df_one'] = units_per_product(df).head(10).to_html(
                                                                    classes="table table-bordered", 
                                                                    index=False
                                                                   )
        context['df_two'] = top_sales(df).head(10).to_html(
                                                            classes="table table-bordered", 
                                                            index=False
                                                            )

        context['df_three'] = top_user(df).head(10).to_html(
                                                            classes="table table-bordered", 
                                                            index=False
                                                            )

        return context
    

def PredictionView(request):
    # trabajamos siempre sobre el ultimo dataset
    document = Document.objects.all().last()
    # esto seria más util como un detail view
    prediction(document)
    return HttpResponse("Tu modelo de prediccion ha sido generado, Por favor regresa al sitio. ")