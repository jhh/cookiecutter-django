{% if not cookiecutter.use_crispy_forms -%}
from django.shortcuts import render

def home_page_view(request):
    return render(request, "index.html")
{% else -%}
import json

from django.http import HttpResponse
from django.shortcuts import render

from .forms import ExampleForm


def home_page_view(request):
    if request.method == "POST":
        form = ExampleForm(request.POST)
        if form.is_valid():
            return HttpResponse("<pre>" + json.dumps(form.cleaned_data, indent=2) + "</pre>")
    else:
        form = ExampleForm()
    return render(request, "index.html", {"example_form": form})
{%- endif %}