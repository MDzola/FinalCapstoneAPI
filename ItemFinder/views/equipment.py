from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ItemFinder.models import Equipment

class EquipmentSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for park areas
    Arguments:
        serializers
    """
    class Meta:
        model = Equipment
        url = serializers.HyperlinkedIdentityField(
            view_name='equipment',
            lookup_field='id'
        )
        fields = ('id', 'url', 'name', 'manufacturer', 'manufacturer_contact')


class Equipments(ViewSet):

    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized product category instance
        """
        new_equipment = Equipment()
        new_equipment.name = request.data["name"]
        new_equipment.manufacturer = request.data["manufacturer"]
        new_equipment.manufacturer_contact = request.data["manufacturer_contact"]
        new_equipment.save()

        serializer = EquipmentSerializer(new_equipment, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single park area
        Returns:
            Response -- JSON serialized park area instance
        """
        try:
            equipment = Equipment.objects.get(pk=pk)
            serializer = EquipmentSerializer(equipment, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to park ProductCategorys resource
        Returns:
            Response -- JSON serialized list of park ProductCategorys
        """
        all_equipment = Equipment.objects.all()

        serializer = EquipmentSerializer(
            all_equipment, many=True, context={'request': request})
        return Response(serializer.data)