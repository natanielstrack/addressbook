import http.client
from httplib2 import Http
import json
import urllib

from oauth2client.service_account import ServiceAccountCredentials

from django.views.generic import View, TemplateView
from django.http import HttpResponse, JsonResponse
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
            conn.close()
            if data['status'] != 'ZERO_RESULTS':
                return True
        except Exception as error:
            print(error)

        return False

    def _read_from_fusion(self, lat, lng):
        scopes = ['https://www.googleapis.com/auth/fusiontables.readonly']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            'AddressBook-777ffbfa3cdb.json', scopes=scopes)
        http_auth = credentials.authorize(Http())

        query_string = '{}?sql={}&key={}'.format(
                'fusiontables/v2/query',
                'SELECT * FROM 1z4oT18gGaoHWbnk08SV6hhOA99xC3OdheXulCjSW'.replace(' ', '%20'),
                settings.GOOGLE_GEO_API_KEY)
        resp, content_json = http_auth.request(
            "https://www.googleapis.com/{}".format(query_string), "GET")
        content = json.loads(content_json.decode('utf-8'))

    def _insert_into_fusion(self, lat, lng):
        scopes = ['https://www.googleapis.com/auth/fusiontables']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            'AddressBook-777ffbfa3cdb.json', scopes=scopes)
        http_auth = credentials.authorize(Http())
        resp, content_json = http_auth.request(
            "https://www.googleapis.com/fusiontables/v2/query",
            "POST",
            'sql=insert into 1z4oT18gGaoHWbnk08SV6hhOA99xC3OdheXulCjSW (location) values ({},{})'.format(lat,lng)
        )
        content = json.loads(content_json.decode('utf-8'))

    def post(self, request, *args, **kwargs):
        lat, lng = request.POST.get('lat'), request.POST.get('lng')
        #self._insert_into_fusion(lat, lng)
        if (lat and lng) and self._is_valid_location(lat, lng):
            Address.objects.create(latitude=lat, longitude=lng)
            #self._insert_into_fusion(lat, lng)
            results = Address.objects.values_list()
            return JsonResponse({'results':list(results)})
        else:
            return HttpResponse(status=404)


class DeleteAddress(View):

    def post(self, request, *args, **kwargs):
        Address.objects.all().delete()

        return HttpResponse("test")


class ListAddress(View):

    def post(self, request, *args, **kwargs):
        results = Address.objects.values_list()
        return JsonResponse({'results':list(results)})
