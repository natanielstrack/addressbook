from django.views.generic import View, TemplateView
from django.http import HttpResponse

from maps.models import Address

class HomeView(TemplateView):
    template_name = "base.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['addresses'] = Address.objects.all()
        return context

class AddAddress(View):

    def post(self, request, *args, **kwargs):
        lat, lng = request.POST.get('lat'), request.POST.get('lng')
        print(lat, lng)
        if lat and lng:
            Address.objects.create(latitude=lat, longitude=lng)

        return HttpResponse("test")

class DeleteAddress(View):

    def post(self, request, *args, **kwargs):
        Address.objects.all().delete()

        return HttpResponse("test")
