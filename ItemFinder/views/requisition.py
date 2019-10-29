"""View module for handling requests about orders"""
from django.http import HttpResponseServerError
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ItemFinder.models import Requisition, Employee, RequisitionItem, SpareItem
from .orderproduct import OrderProductSerializer
from .product import ProductSerializer


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for Orders

    Arguments:
        serializers
    """
    class Meta:
        model = Requisition
        url = serializers.HyperlinkedIdentityField(
            view_name='requisition',
            lookup_field='id'
        )
        fields = ('id', 'url', 'employee', 'spareitem')
        depth = 1

class Orders(ViewSet):
    """Orders for Bangazon API"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Order instance
        """
        order_item = OrderProduct()
        order_item.product = Product.objects.get(pk=request.data["id"])

        current_customer = Customer.objects.get(user=request.auth.user)
        order = Order.objects.filter(customer=current_customer, paymenttype__isnull=True)

        if order.exists():
            print("open order in db. Add it and the prod to OrderProduct")
            order_item.order = order[0]
        else:
            print("no open orders. Time to make a new order to add this product to")
            new_order = Order()
            new_order.customer = current_customer
            new_order.save()
            order_item.order = new_order

        order_item.save()

        serializer = OrderProductSerializer(order_item, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single order

        Returns:
            Response -- JSON serialized order instance
        """
        try:
            order = Order.objects.get(pk=pk)
            serializer = OrderSerializer(order, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for an Order

        Returns:
            Response -- Empty body with 204 status code
        """
        order = Order.objects.get(pk=pk)
        payment = PaymentType.objects.get(pk=request.data["payment_id"])
        order.payment = payment
        order.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single order are

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            order = Order.objects.get(pk=pk)
            order.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Order.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['get', 'put', 'delete'], detail=False)
    def cart(self, request):
        """Handle GET one cart from logged in user

        Returns:
            Response -- JSON serialized list of products and order
        """
        current_user = Customer.objects.get(user=request.auth.user)
        if request.method == "GET":



            try:
                open_order = Order.objects.get(customer=current_user, paymenttype=None)
                products_on_order = Product.objects.filter(cart__order=open_order)
            except Order.DoesNotExist as ex:
                return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

            serializer = ProductSerializer(products_on_order, many=True, context={'request': request})
            return Response(serializer.data)

        if request.method == "DELETE":
                try:
                    open_order = Order.objects.get(customer=current_user, paymenttype=None)
                    open_order.delete()

                    return Response({}, status=status.HTTP_204_NO_CONTENT)
                except Order.DoesNotExist as ex:
                    return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
                except Exception as ex:
                    return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        if request.method == "PUT":

            if "payment_id" in request.data:
                try:
                    open_order = Order.objects.get(customer=current_user, paymenttype=None)
                    payment_id = PaymentType.objects.get(pk=request.data["payment_id"])
                    open_order.paymenttype = payment_id
                    open_order.save()
                    return Response({}, status=status.HTTP_204_NO_CONTENT)

                except Order.DoesNotExist as ex:
                    return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

            if "product_id" in request.data:

                try:
                    open_order = Order.objects.get(customer=current_user, paymenttype=None)
                    product = Product.objects.get(pk=request.data["product_id"])
                    delete_me = OrderProduct.objects.filter(product=product, order=open_order)[0]
                    delete_me.delete()

                except Order.DoesNotExist as ex:
                    return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

                return Response({}, status=status.HTTP_204_NO_CONTENT)


    def list(self, request):
        """Handle GET requests to orders resource

        Returns:
            Response -- JSON serialized list of orders
        """
        orders = Order.objects.all()
        customer = Customer.objects.get(pk=request.auth.user.id)
        # (pk=request.auth.user)

        cart = self.request.query_params.get('cart', None)
        orders = orders.filter(customer=customer, paymenttype=None)
        print("orders", orders)
        if cart is not None:
            orders = orders.filter(paymenttype=None).get()
            print("orders filtered", orders)
            serializer = OrderSerializer(
                orders, many=False, context={'request': request}
            )

        else:
            serializer = OrderSerializer(
                orders, many=True, context={'request': request}
            )
        serializer = OrderSerializer(orders, many=True, context={'request': request})


        return Response(serializer.data)