from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import CreateView


# Create your views here.

class LiveGame(TemplateView):
    template_name = "base.html"

    def message(request):
        return render(request, 'ssp/sspTableView.html', {'message': "HELLO WORLD"})


def index(request):
    return render(request, "base.html")
