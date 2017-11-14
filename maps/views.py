import json
from rest_framework import viewsets

from django.views.generic import View, TemplateView
from django.http import HttpResponse, JsonResponse
from django.conf import settings

from maps.models import Address
from maps.utils import FusiontablesHandler
from maps.serializers import AddressSerializer


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['addresses'] = Address.objects.all()
        context['google_geo_api_key'] = settings.GOOGLE_GEO_API_KEY
        context['fusion_table_id'] = settings.FUSION_TABLE_ID
        context['root_url'] = '/api/address/'
        return context


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    def delete(self, request, *args, **kwargs):
        try:
            fusiontables = FusiontablesHandler()
            fusiontables.delete()

            Address.objects.all().delete()
            return HttpResponse(status=200)
        except:
            return HttpResponse(status=404)
