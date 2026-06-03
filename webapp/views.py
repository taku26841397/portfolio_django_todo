from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class MenuPageView(LoginRequiredMixin,TemplateView):
    template_name='menu.html'