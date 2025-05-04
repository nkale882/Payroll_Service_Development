from rest_framework import serializers
from payroll_app.models import User
from payroll_app.models import Employer
from .models import Position



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']
    
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class UserSignupSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone_number= serializers.IntegerField()
    email = serializers.EmailField()
    password = serializers.CharField()
    #position= serializers.IntegerField()

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        return user

class EmployerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employer
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']
    
class EmployerLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class EmployerSignupSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone_number= serializers.IntegerField()
    email = serializers.EmailField()
    password = serializers.CharField()

    def create(self, validated_data):
        employer = Employer.objects.create(**validated_data)
        return employer
    
class UserVerificationSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ['id','annual_salary']
            #read_only_fields = ['id'] 

class UserverificationGet(serializers.ModelSerializer):
    class Meta:
        model = User
        fields= ['id','first_name', 'last_name', 'phone_number', 'email', 'password']


from .models import Position
class positionserializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'



from .models import LeaveManagement
from datetime import date
class LeaveManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveManagement
        fields = ['user', 'date']

class LeaveManagementSerializerGet(serializers.ModelSerializer):
    class Meta:
        model = LeaveManagement
        fields= '__all__'


class UpdateLeaveStatusSerializer(serializers.Serializer):
    APPROVED = 'approved'
    REJECTED = 'rejected'
    
    STATUS_CHOICES = [
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
    ]
    
    status = serializers.ChoiceField(choices=STATUS_CHOICES)

from. models import Loss_of_pay_leaveLeaveManagement
class LossOfPayLeaveManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loss_of_pay_leaveLeaveManagement
        fields = ['user', 'date']

class Loss_of_pay_LeaveManagementSerializerGet(serializers.ModelSerializer):
    class Meta:
        model = LeaveManagement
        fields= '__all__'

class Update_loss_of_pay_LeaveStatusSerializer(serializers.Serializer):
    APPROVED = 'approved'
    REJECTED = 'rejected'
    
    STATUS_CHOICES = [
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
    ]
    
    status = serializers.ChoiceField(choices=STATUS_CHOICES)


class UserAnnualSalaryRevisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['annual_salary']

from .models import PayrollManagement

class PayrollManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayrollManagement
        fields = '__all__'

class PayrollCalculationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayrollManagement
        MONTH_CHOICES = (
        (1, 'January'),
        (2, 'February'),
        (3, 'March'),
        (4, 'April'),
        (5, 'May'),
        (6, 'June'),
        (7, 'July'),
        (8, 'August'),
        (9, 'September'),
        (10, 'October'),
        (11, 'November'),
        (12, 'December'),
         )
        month=serializers.ChoiceField(choices=MONTH_CHOICES)
        fields = ['user', 'year', 'month']

        