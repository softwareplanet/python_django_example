from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from employee.model_views import MultipleInstanceAPIView, SingleInstanceAPIView
from employee.models import Employee
from employee.permissions import IsAdminOrSelf, IsPostOrIsAdmin
from employee.search_serializers import SearchEmployeeSerializer
from employee.serializers import EmployeeSerializer, EmployeeForUserSerializer, ChangePasswordSerializer
from employee.utils import Utils


class ListEmployees(MultipleInstanceAPIView):
    serializer = EmployeeForUserSerializer
    model = Employee
    permission_classes = (IsPostOrIsAdmin,)

    def get(self, request):
        models = self.model.objects
        return Response(self.serializer(models, many=True).data)


class ListEmployee(SingleInstanceAPIView):
    serializer = EmployeeSerializer
    serializer_for_user = EmployeeForUserSerializer
    model = Employee
    permission_classes = (permissions.IsAuthenticated, IsAdminOrSelf)

    def put(self, request, model_id):
        try:
            employee = self.model.objects.get(id=model_id)
            employee.is_active = True
            employee.save()

            return Response(self.serializer_for_user(employee).data, status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            return Utils.error_response(e.args, status.HTTP_404_NOT_FOUND)

    def delete(self, request, model_id):
        try:
            model = self.model.objects.get(id=model_id)
            model.is_active = False
            model.save()
            return Response({'id': model_id}, status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            return Utils.error_response(e.args, status.HTTP_404_NOT_FOUND)


class ListMe(APIView):
    serializer = EmployeeForUserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        return Response(EmployeeForUserSerializer(request.user).data)

    def patch(self, request):
        try:
            model = request.user
            serializer = self.serializer(model, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status.HTTP_200_OK)
            else:
                return Utils.error_response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist as e:
            return Utils.error_response(e.args, status.HTTP_404_NOT_FOUND)

    def put(self, request):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.data.get("old_password")
            if not user.check_password(old_password):
                return Utils.error_response({"old_password": ["Wrong password."]}, status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.data.get("new_password"))
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Utils.error_response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class ListSearch(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        from django.db.models import Q
        result = []
        data = request.data['query']
        if request.user.is_staff:
            result.extend(SearchEmployeeSerializer(
                Employee.objects.filter(
                    Q(first_name__icontains=data) | Q(last_name__icontains=data) | Q(
                        description__icontains=(' ' + data)) | Q(description__istartswith=data)),
                many=True).data)
        else:
            pass
        return Response(result)
