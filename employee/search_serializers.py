from rest_framework import serializers

from employee.models import Employee


class SearchEmployeeSerializer(serializers.HyperlinkedModelSerializer):
    firstName = serializers.CharField(source='first_name', required=True)
    lastName = serializers.CharField(source='last_name', required=True)
    isActive = serializers.BooleanField(source='is_active')

    def to_representation(self, obj):
        data = super().to_representation(obj)
        data['type'] = 'employee'
        return data

    class Meta:
        model = Employee
        fields = ('id', 'firstName', 'lastName', 'image', 'description', 'isActive')
