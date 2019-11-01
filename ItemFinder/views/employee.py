"""View module for handling requests about park areas"""
from django.http import HttpResponseServerError
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ItemFinder.models import Employee


class EmployeeSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for Customers

    Arguments:
        serializers
    """
    class Meta:
        model = Employee
        url = serializers.HyperlinkedIdentityField(
            view_name='employee',
            lookup_field='id'
        )
        fields = ('id', 'url', 'phone_number', 'title', 'user', 'user_id')
        depth = 1


class Employees(ViewSet):

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Attraction instance
        """
        new_employee = Employee()
        new_employee.phone_number = request.data["phone_number"]
        new_employee.address = request.data["title"]
        new_employee.user_id = request.data["user_id"]

        new_employee.save()

        serializer = CustomerSerializer(new_employee, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single park area

        Returns:
            Response -- JSON serialized park area instance
        """
        try:
            employee = Employee.objects.get(pk=pk)
            serializer = EmployeeSerializer(employee, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):

        employees = Employee.objects.all()

        user_id = self.request.query_params.get('employee', None)
        if user_id is not None:
            employees = employees.filter(user__id=user_id)

        serializer = EmployeeSerializer(
            employees, many=True, context={'request': request})
        return Response(serializer.data)

    @action(methods=['get', 'put'], detail=False)
    def currentEmployee(self, request, pk=None):

        if request.method == "GET":

            try:
                employee = Employee.objects.get(user=request.auth.user)
            except Employee.DoesNotExist as ex:
                return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

            serializer = EmployeeSerializer(employee, context={'request': request})
            return Response(serializer.data)

        if request.method == "PUT":

            try:
                update_employee = Employee.objects.get(user=request.auth.user)
                title = request.data["title"]
                phone_number = request.data["phone_number"]
                update_employee.title = title
                update_employee.phone_number = phone_number
                update_employee.save()
                return Response({}, status=status.HTTP_204_NO_CONTENT)

            except Employee.DoesNotExist as ex:
                return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
