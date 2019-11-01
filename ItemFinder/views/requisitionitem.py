"""View module for handling requests about park areas"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ItemFinder.models import RequisitionOrder, SpareItem, RequisitionItem, Employee


class RequisitionItemSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = RequisitionItem
        url = serializers.HyperlinkedIdentityField(
            view_name='requisitionitem',
            lookup_field='id'
        )
        fields = ('id', 'url', 'requisitionOrder', 'spareItem')
        depth = 1

class RequisitionItems(ViewSet):

    def create(self, request):

        new_requisition_item = RequisitionItem()
        requisition_order = RequisitionOrder.objects.get(pk=request.data["requisition_order_id"])
        requisition_item = SpareItem.objects.get(pk=request.data["spare_item_id"])

        new_requisition_item.requisitionOrder = requisition_order
        new_requisition_item.spareItem = requisition_item
        new_requisition_item.save()

        serializer = RequisitionItemSerializer(new_requisition_item, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):

        try:
            requisitionitem = RequisitionItem.objects.get(pk=pk)
            serializer = RequisitionItemSerializer(requisitionitem, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):

        requisition_item = RequisitionItem.objects.get(pk=pk)
        requisition_order = RequisitionOrder.objects.get(pk=request.data["requisition_order_id"])
        spare_item = SpareItem.objects.get(pk=request.data["spare_item_id"])

        requisition_item.requisitionOrder = requisition_order
        requisition_item.spareItem = spare_item
        requisition_item.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single park are

        Returns:
            Response -- 200, 404, or 500 status code
            how to get current users open order
        """
        try:

            requisition_item = RequisitionItem.objects.get(pk=pk)
            requisition_item.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except RequisitionItem.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to park attractions resource

        Returns:
            Response -- JSON serialized list of park attractions
        """
        requisition_items = RequisitionItem.objects.all()

        requisitionOrder = self.request.query_params.get('requisition_order', None)
        spareItem = self.request.query_params.get('spare_item', None)
        isComplete = self.request.query_params.get('isComplete', None)

        if spareItem is not None:
            requisition_items = requisition_items.filter(spareItem__id=spareItem)
        if requisitionOrder is not None:
            requisition_items = requisition_items.filter(isComplete=False)

        serializer = RequisitionItemSerializer(
            requisition_items, many=True, context={'request': request})
        return Response(serializer.data)
