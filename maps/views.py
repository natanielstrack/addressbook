import http.client
import json

from django.views.generic import View, TemplateView
from django.http import HttpResponse
from django.conf import settings

from maps.models import Address

class HomeView(TemplateView):
    template_name = "base.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['addresses'] = Address.objects.all()
        return context

class AddAddress(View):

    def _is_valid_location(self, lat, lng):
        try:
            conn = http.client.HTTPSConnection("maps.googleapis.com")
            query_string = '{}?location={},{}&radius=500&key={}'.format(
                settings.GOOGLE_GEO_URL, lat, lng, settings.GOOGLE_GEO_API_KEY)
            conn.request("GET", query_string)
            response = conn.getresponse()
            data = json.loads(response.read().decode('utf-8'))
            if data['status'] != 'ZERO_RESULTS':
                return True
        except Exception:
            pass

        return False

    def post(self, request, *args, **kwargs):
        lat, lng = request.POST.get('lat'), request.POST.get('lng')
        if (lat and lng) and self._is_valid_location(lat, lng):
            Address.objects.create(latitude=lat, longitude=lng)

        return HttpResponse("test")

class DeleteAddress(View):

    def post(self, request, *args, **kwargs):
        Address.objects.all().delete()

        return HttpResponse("test")
