import googlemaps
import json

from httplib2 import Http
from oauth2client.service_account import ServiceAccountCredentials

from django.conf import settings

INSERT = 'insert'
SELECT = 'select'
DELETE = 'delete'


class PlacesHandler:
    def get_address(self, lat, lng):
        try:
            gmaps = googlemaps.Client(key=settings.GOOGLE_GEO_API_KEY)
            reverse_geocode_result = gmaps.reverse_geocode(
                (lat, lng), location_type='ROOFTOP')
            return reverse_geocode_result[0]['formatted_address']
        except Exception as error:
            print(error)
        return None


class FusiontablesHandler:
    access_token = ''
    http_auth = Http()
    table_key = settings.FUSION_TABLE_ID
    fusiontables_url = settings.FUSION_TABLES_URL

    def __init__(self):
        scopes = ['https://www.googleapis.com/auth/fusiontables']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            settings.GOOGLE_SERVICE_ACCOUNT_FILE, scopes=scopes)
        credentials.get_access_token()

        self.http_auth = credentials.authorize(Http())
        self.access_token = credentials.access_token

    def _build_url(self, latitude, longitude, request_type=SELECT):
        if latitude and longitude:
            lat_str = str(round(float(latitude),7))
            lng_str = str(round(float(longitude),7))

        sentence = ''
        if request_type == INSERT:
            sentence = "insert into {} (location) values ('{},{}')".format(
                self.table_key, lat_str, lng_str)
        elif request_type == DELETE:
            sentence = "delete from {}".format(self.table_key)
        else:
            sentence = "select * from {} where location = '{},{}'".format(
                self.table_key, lat_str, lng_str)
        sentence = sentence.replace(' ', '%20')

        return "{}?sql={}".format(self.fusiontables_url, sentence)

    def _make_request(
        self, latitude=None, longitude=None, request_type=SELECT
    ):
        url = self._build_url(latitude, longitude, request_type)
        http_method = "GET" if request_type == SELECT else "POST"
        headers = {
                'content-type':'application/json',
                'Content-Length':0
            }

        resp, content_json = self.http_auth.request(
            url, http_method, headers=headers)
        return json.loads(content_json.decode('utf-8'))

    def location_exists(self, latitude, longitude):
        result = self._make_request(latitude, longitude)

        return 'rows' in result

    def delete(self):
        result = self._make_request(request_type=DELETE)
        print(result)

        return 'rows' in result

    def insert(self, latitude, longitude):
        if not self.location_exists(latitude, longitude):
            result = self._make_request(latitude, longitude, INSERT)

            if not 'rows' in result:
                raise Exception('Could not insert data into Fustiontable')
        else:
            return
