from rest_framework import serializers

from maps.models import Address
from maps.utils import PlacesHandler, FusiontablesHandler


class AddressSerializer(serializers.ModelSerializer):
    address = serializers.CharField(required=False)

    class Meta:
        model = Address
        fields = ('latitude', 'longitude', 'address')

    def create(self, validated_data):
        latitude = validated_data.get('latitude')
        longitude = validated_data.get('longitude')

        places = PlacesHandler()
        address = places.get_address(latitude, longitude)
        
        if not address:
            raise serializers.ValidationError(
                'No address found on this location')

        fusiontables = FusiontablesHandler()
        fusiontables.insert(latitude, longitude)

        return Address.objects.create(
            latitude=latitude,
            longitude=longitude,
            address=address
        )
