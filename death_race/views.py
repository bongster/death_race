from django.shortcuts import render
from django.views.generic import TemplateView, RedirectView

# Create your views here.

class MainRedirectView(RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'game-detail'

    def get_redirect_url(self, *args, **kwargs):
        kwargs['pk'] = kwargs.get('pk') or 1
        print(kwargs)
        return super().get_redirect_url(*args, **kwargs)

class MainView(TemplateView):
    template_name = 'main.html'
