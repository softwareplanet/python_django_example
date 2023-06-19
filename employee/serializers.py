from rest_framework import serializers

from employee.models import Employee


class EmployeeSerializer(serializers.HyperlinkedModelSerializer):
    firstName = serializers.CharField(source='first_name', required=True)
    lastName = serializers.CharField(source='last_name', required=True)
    careerStartDate = serializers.CharField(source='career_start_date', required=False)
    password = serializers.CharField(write_only=True, required=True)
    isStaff = serializers.BooleanField(source='is_staff', required=False)
    isActive = serializers.BooleanField(source='is_active', read_only=False)
    skills = serializers.SerializerMethodField(read_only=True)
    projects = serializers.SerializerMethodField()

    @staticmethod
    def validate_password(value):
        from django.contrib.auth.password_validation import validate_password
        validate_password(value)
        return value

    @staticmethod
    def get_skills(obj):
        return [skill.name for skill in obj.skills.all()]

    @staticmethod
    def get_projects(obj):
        projects = []
        for project in obj.projects.distinct():
            projects.append(project.name)
        return projects

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance

    class Meta:
        model = Employee
        fields = (
            'id', 'username', 'email', 'password', 'firstName', 'lastName', 'dob',
            'isStaff', 'image', 'description', 'skills', 'projects', 'careerStartDate', 'position', 'isActive'
        )


class EmployeeForUserSerializer(EmployeeSerializer):
    isStaff = serializers.BooleanField(read_only=True, source='is_staff')
    isActive = serializers.BooleanField(read_only=True, source='is_active')

    class Meta(EmployeeSerializer.Meta):
        fields = (
            'id', 'username', 'email', 'password', 'firstName', 'lastName', 'dob',
            'isStaff', 'image', 'skills', 'projects', 'careerStartDate', 'position',
            'isActive'
        )


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        from django.contrib.auth.password_validation import validate_password
        validate_password(value)
        return value

