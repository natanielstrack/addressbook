import googlemaps
import json

from django.views.generic import View, TemplateView
from django.http import HttpResponse, JsonResponse
from django.conf import settings

from maps.models import Address


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['addresses'] = Address.objects.all()
        context['google_geo_api_key'] = settings.GOOGLE_GEO_API_KEY
        context['fusion_table_id'] = settings.FUSION_TABLE_ID
        return context


class AddAddress(View):

    def _get_address(self, lat, lng):
        try:
            gmaps = googlemaps.Client(key=settings.GOOGLE_GEO_API_KEY)
            reverse_geocode_result = gmaps.reverse_geocode((lat, lng))
            return reverse_geocode_result[0]['formatted_address']
        except Exception as error:
            print(error)
        return None

    def post(self, request, *args, **kwargs):
        lat, lng = request.POST.get('lat'), request.POST.get('lng')
        formatted_address = self._get_address(lat, lng)
        if formatted_address:
            Address.objects.create(
                latitude=lat,
                longitude=lng,
                address=formatted_address)
            results = Address.objects.values_list()
            return JsonResponse({'results':list(results)})
        else:
            return HttpResponse(status=404)


class DeleteAddress(View):

    def post(self, request, *args, **kwargs):
        try:
            Address.objects.all().delete()
            return HttpResponse(status=200)
        except:
            return HttpResponse(status=404)


class ListAddress(View):

    def post(self, request, *args, **kwargs):
        results = Address.objects.values_list()
        return JsonResponse({'results':list(results)})
