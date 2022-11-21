import logging

from django.views.generic import TemplateView


logger = logging.getLogger(__name__)


class HomeView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context["welcome_message"] = "Greetings!"
        return context


class AboutView(TemplateView):
    template_name = "pages/about.html"
