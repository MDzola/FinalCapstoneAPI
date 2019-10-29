from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ItemFinder.models import ItemCategory

class ItemCategorySerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for park areas
    Arguments:
        serializers
    """
    class Meta:
        model = ItemCategory
        url = serializers.HyperlinkedIdentityField(
            view_name='itemcategory',
            lookup_field='id'
        )
        fields = ('id', 'url', 'name')


class ItemCategories(ViewSet):

    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized product category instance
        """
        new_item_category = ItemCategory()
        new_item_category.name = request.data["name"]
        new_item_category.save()

        serializer = ItemCategorySerializer(new_item_category, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single park area
        Returns:
            Response -- JSON serialized park area instance
        """
        try:
            category = ItemCategory.objects.get(pk=pk)
            serializer = ItemCategorySerializer(category, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to park ProductCategorys resource
        Returns:
            Response -- JSON serialized list of park ProductCategorys
        """
        item_category = ItemCategory.objects.all()

        serializer = ItemCategorySerializer(
            item_category, many=True, context={'request': request})
        return Response(serializer.data)