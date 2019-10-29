"""View module for handling requests about orders"""
from django.http import HttpResponseServerError
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ItemFinder.models import RequisitionOrder, Employee, RequisitionItem, SpareItem
from .spareitem import SpareItemSerializer


class RequisitionOrderSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for Orders

    Arguments:
        serializers
    """
    class Meta:
        model = RequisitionOrder
        url = serializers.HyperlinkedIdentityField(
            view_name='requisitionorder',
            lookup_field='id'
        )
        fields = ('id', 'url', 'employee', 'spareitem')
        depth = 1

class RequisitionOrders(ViewSet):
    """Orders for Bangazon API"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Order instance
        """
        spare_item = RequisitionItem()
        spare_item.spareItem = SpareItem.objects.get(pk=request.data["id"])

        employee = Employee.objects.get(user=request.auth.user)
        requisitionOrder = RequisitionOrder.objects.filter(employee=employee, isComplete__isFalse=True)

        if requisitionOrder.exists():
            print("open order in db. Add it and the prod to OrderProduct")
            spare_item.requisition = requisition[0]
        else:
            print("no open orders. Time to make a new order to add this product to")
            new_requisition_order = RequisitionOrder()
            new_requisition_order.employee = employee
            spare_item.order = new_requisition_order
            new_requisition_order.save()

        spare_item.save()

        serializer = RequisitionOrderSerializer(spare_item, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single order

        Returns:
            Response -- JSON serialized order instance
        """
        try:
            requisition = RequisitionOrder.objects.get(pk=pk)
            serializer = RequisitionOrderSerializer(requisition, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for an Order

        Returns:
            Response -- Empty body with 204 status code
        """
        requisition = RequisitionOrder.objects.get(pk=pk)
        isComplete = True
        requisition.isComplete = isComplete
        requisition.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single order are

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            requisition = RequisitionOrder.objects.get(pk=pk)
            requisition.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except RequisitionOrder.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['get'], detail=False)
    def cart(self, request):
        """Handle GET one cart from logged in user

        Returns:
            Response -- JSON serialized list of products and order
        """
        employee = Employee.objects.get(user=request.auth.user)

        if request.method == "GET":



            try:
                open_requisition_order = RequisitionOrder.objects.get(employee=employee, isComplete="False")
                items_on_requisition = SpareItem.objects.filter(cart__order=open_requisition_order)
            except RequisitionOrder.DoesNotExist as ex:
                return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

            serializer = SpareItemSerializer(items_on_requisition, many=True, context={'request': request})
            return Response(serializer.data)


    def list(self, request):
        """Handle GET requests to orders resource

        Returns:
            Response -- JSON serialized list of orders
        """
        requisitions = RequisitionOrder.objects.all()
        employee = Employee.objects.get(pk=request.auth.user.id)
        # (pk=request.auth.user)

        cart = self.request.query_params.get('cart', None)
        requisitions = requisitions.filter(employee=employee, isComplete="False")
        print("requisitions", requisitions)
        if cart is not None:
            requisitions = requisitions.filter(isComplete="False").get()
            print("requisitions filtered", requisitions)
            serializer = RequisitionOrderSerializer(
                requisitions, many=False, context={'request': request}
            )

        else:
            serializer = RequisitionOrderSerializer(
                requisitions, many=True, context={'request': request}
            )
        serializer = RequisitionOrderSerializer(requisitions, many=True, context={'request': request})


        return Response(serializer.data)