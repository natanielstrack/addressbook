from django.views.generic import TemplateView

from maps.models import Address

class HomeView(TemplateView):
    template_name = "base.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['addresses'] = Address.objects.all()
        return context
