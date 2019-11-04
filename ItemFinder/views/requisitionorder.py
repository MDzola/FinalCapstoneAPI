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
    """JSON serializer for Requisitions

    Arguments:
        serializers
    """
    class Meta:
        model = RequisitionOrder
        url = serializers.HyperlinkedIdentityField(
            view_name='requisitionorder',
            lookup_field='id'
        )
        fields = ('id', 'url', 'employee', 'isComplete', 'spare_item')
        depth = 1

class RequisitionOrders(ViewSet):


    def create(self, request):

        spare_item = RequisitionItem()
        spare_item.spareItem = SpareItem.objects.get(pk=request.data["id"])

        employee = Employee.objects.get(user=request.auth.user)
        requisitionOrder = RequisitionOrder.objects.filter(employee=employee, isComplete=False)

        if requisitionOrder.exists():
            print("open order in db. Add it and the prod to OrderProduct")
            spare_item.requisitionOrder= requisitionOrder[0]
        else:
            print("no open orders. Time to make a new order to add this product to")
            new_requisition_order = RequisitionOrder()
            new_requisition_order.employee = employee
            new_requisition_order.save()
            spare_item.order = new_requisition_order

        spare_item.save()

        serializer = RequisitionOrderSerializer(spare_item, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):

        try:
            requisition = RequisitionOrder.objects.get(pk=pk)
            serializer = RequisitionOrderSerializer(requisition, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):

        requisition = RequisitionOrder.objects.get(pk=pk)
        isComplete = True
        requisition.isComplete = isComplete
        requisition.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):

        try:
            requisition = RequisitionOrder.objects.get(pk=pk)
            requisition.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except RequisitionOrder.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['get', 'put', 'delete'], detail=False)
    def cart(self, request):

        employee = Employee.objects.get(user=request.auth.user)

        if request.method == "GET":

            try:
                open_requisition_order = RequisitionOrder.objects.get(employee=employee, isComplete=False)
                items_on_requisition = SpareItem.objects.filter(cart__requisitionOrder=open_requisition_order)
            except RequisitionOrder.DoesNotExist as ex:
                return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

            serializer = SpareItemSerializer(items_on_requisition, many=True, context={'request': request})
            return Response(serializer.data)

        if request.method == "DELETE":
                try:
                    open_requisition_order = RequisitionOrder.objects.get(employee=employee, isComplete=False)
                    open_requisition_order.delete()

                    return Response({}, status=status.HTTP_204_NO_CONTENT)
                except RequisitionOrder.DoesNotExist as ex:
                    return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
                except Exception as ex:
                    return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        if request.method == "PUT":

            if "is_complete" in request.data:
                try:
                    open_requisition_order = RequisitionOrder.objects.get(employee=employee, isComplete=False)
                    items_on_requisition = open_requisition_order.cart.all()
                    items_on_requisition_set = set()
                    open_requisition_order.isComplete = True
                    open_requisition_order.save()

                    if open_requisition_order.isComplete:
                        for ir in items_on_requisition:
                            items_on_requisition_set.add(ir.spareItem)

                        spareItems = list(items_on_requisition_set)

                        for i in spareItems:
                            num_sold = i.cart.filter(requisitionOrder=open_requisition_order).count()
                            i.quantity = i.new_inventory(num_sold)
                            i.save()

                    return Response({}, status=status.HTTP_204_NO_CONTENT)

                except RequisitionOrder.DoesNotExist as ex:
                    return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


            if "spareItem_id" in request.data:

                try:
                    open_requisition_order = RequisitionOrder.objects.get(employee=employee, isComplete=False)
                    spare_item = SpareItem.objects.get(pk=request.data["spareItem_id"])
                    delete_me = RequisitionItem.objects.filter(spareItem=spare_item, requisitionOrder=open_requisition_order)[0]
                    delete_me.delete()

                except RequisitionOrder.DoesNotExist as ex:
                    return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

                return Response({}, status=status.HTTP_204_NO_CONTENT)

    def list(self, request):

        requisitions = RequisitionOrder.objects.all()
        employee = Employee.objects.get(user=request.auth.user)

        cart = self.request.query_params.get('cart', None)
        requisitions = requisitions.filter(employee=employee, isComplete=False)
        print("requisitions", requisitions)
        if cart is not None:
            requisitions = requisitions.filter(isComplete=False).get()
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