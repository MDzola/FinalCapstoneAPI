"""View module for handling requests about park areas"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action
from ItemFinder.models import SpareItem, Employee, ItemCategory



class SpareItemSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for park areas

    Arguments:
        serializers
    """
    class Meta:
        model = SpareItem
        url = serializers.HyperlinkedIdentityField(
            view_name='spareitem',
            lookup_field='id'
        )
        # This fields method is to pull every attribute or piece of data from an instance of a created Model
        fields = ('id', 'url', 'name', 'description', 'quantity', 'critical_quantity', 'category')
        depth = 1


class SpareItems(ViewSet):
    """Products for Bangazon API"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Attraction instance
        """
        new_spare_item = SpareItem()
        new_spare_item.name = request.data["name"]
        new_spare_item.description = request.data["description"]
        new_spare_item.quantity = request.data["quantity"]
        new_spare_item.critical_quantity = request.data["critical_quantity"]
        category = ItemCategory.objects.get(pk=request.data["itemcategory_id"])

        new_spare_item.category = category
        new_spare_item.save()

        serializer = SpareItemSerializer(new_spare_item, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single park area

        Returns:
            Response -- JSON serialized park area instance
        """
        try:
            spare_item = SpareItem.objects.get(pk=pk)
            serializer = SpareItemSerializer(spare_item, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a park area attraction

        Returns:
            Response -- Empty body with 204 status code
        """
        spare_item_update = SpareItem.objects.get(pk=pk)
        spare_item_update.name = request.data["name"]
        spare_item_update.description = request.data["description"]
        spare_item_update.quantity = request.data["quantity"]
        spare_item_update.critical_quantity = request.data["critical_quantity"]
        category = ItemCategory.objects.get(pk=request.data["itemcategory_id"])

        spare_item_update.category = category
        spare_item_update.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):

        """
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            category = SpareItem.objects.get(pk=pk)
            category.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except SpareItem.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to park attractions resource

        Returns:
            Response -- JSON serialized list of park attractions
        """
        spare_items = SpareItem.objects.all()
        spare_items_list = []

        # Support filtering spare-items by category id
        category = self.request.query_params.get('category', None)
        if category is not None:
            spare_items = spare_items.filter(category__id=category)

        serializer = SpareItemSerializer(
            spare_items, many=True, context={'request': request})
        return Response(serializer.data)


