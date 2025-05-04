from django.shortcuts import render
from rest_framework.decorators import api_view,renderer_classes
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
import datetime
import calendar
from django.core.mail import send_mail

from rest_framework import viewsets

from payroll_app.models import Employer
from payroll_app.seralizers import EmployerSerializer

from payroll_app.models import User
from payroll_app.seralizers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
@api_view(['GET'])
def user_list(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    # elif request.method == 'POST':
    #     serializer = UserSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # if request.method == 'GET':
    #     serializer = UserSerializer(user)
    #     return Response(serializer.data)
    # elif request.method == 'PUT':
    #     serializer = UserSerializer(user, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EmployerViewSet(viewsets.ModelViewSet):
    queryset = Employer.objects.all()
    serializer_class = EmployerSerializer

@api_view(['GET'])
def employer_list(request):
    if request.method == 'GET':
        employees = Employer.objects.all()
        serializer = EmployerSerializer(employees, many=True)
        return Response(serializer.data)

    # elif request.method == 'POST':
    #     serializer = EmployerSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['DELETE'])
def employer_detail(request, pk):
    try:
        employee = Employer.objects.get(pk=pk)
    except Employer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # if request.method == 'GET':
    #     serializer = EmployerSerializer(employee)
    #     return Response(serializer.data)
    # elif request.method == 'PUT':
    #     serializer = EmployerSerializer(employee, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
from .models import Position
from .seralizers import positionserializer

class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = positionserializer

@swagger_auto_schema(methods=['post'],request_body=positionserializer)    
@api_view(['POST'])
def position_list(request):
    if request.method == 'POST':
        serializer = positionserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def position_detail(request, pk):
    try:
        position = Position.objects.get(pk=pk)
    except Position.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = positionserializer(position)
        return Response(serializer.data)

    elif request.method in ['PUT', 'PATCH']:
        serializer = positionserializer(position, data=request.data, partial=request.method == 'PATCH')
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        position.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


from payroll_app.seralizers import UserLoginSerializer,EmployerLoginSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

@swagger_auto_schema(methods=['post'],request_body=UserLoginSerializer)
@api_view(['POST'])
def user_login(request):
    if request.method=='POST':
        Serializer=UserLoginSerializer(data=request.data)
    if Serializer.is_valid():
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user = User.objects.get(email=email,password=password)
        except User.DoesNotExist:
            return Response({'error': 'User does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        if not user.verified:
            return Response({'error': 'User is not verified.'}, status=status.HTTP_401_UNAUTHORIZED)
        if user.password != password or user.email!=email:
            return Response({'error': 'Invalid password or email.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'User login successfully.'}, status=status.HTTP_200_OK)
    return Response(Serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(methods=['post'],request_body=EmployerLoginSerializer)
@api_view(['POST'])
def employer_login(request):
    if request.method == 'POST':
        serializer = EmployerLoginSerializer(data=request.data)
    if serializer.is_valid():
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            employer = Employer.objects.get(email=email,password=password)
        except Employer.DoesNotExist:
            return Response({'error': 'User does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        if employer.password != password or employer.email!=email:
            return Response({'error': 'Invalid password or email.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Employer login successfully.'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from .seralizers import UserSignupSerializer
@swagger_auto_schema(methods=['post'],request_body=UserSignupSerializer)
@api_view(['POST'])
def user_signup(request):
    if request.method == 'POST':
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            # p=serializer.validated_data['position']
            # try:
            #    position= Position.objects.get(id=p)
            # except Position.DoesNotExist:
            #    return Response({"error": "Position not found."}, status=status.HTTP_404_NOT_FOUND)
            user = serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

from .seralizers import EmployerSignupSerializer 
@swagger_auto_schema(methods=['post'],request_body=EmployerSignupSerializer)
@api_view(['POST'])
def employer_signup(request):
    if request.method == 'POST':
        serializer = EmployerSignupSerializer(data=request.data)
        if serializer.is_valid():
            employer = serializer.save()
            return Response("Employer created successfully!", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from .seralizers import UserverificationGet
@swagger_auto_schema(methods=['get'])
@api_view(['GET'])
def get_verified_users(request):
    if request.method == 'GET':
        verified_users = User.objects.filter(verified=True)
        serialized_users = UserverificationGet(verified_users, many=True)
        return Response(serialized_users.data)


@swagger_auto_schema(methods=['get'])
@api_view(['GET'])
def get_unverified_users(request):
    if request.method == 'GET':
        unverified_users = User.objects.filter(verified=False)
        serialized_users = UserverificationGet(unverified_users, many=True)
        return Response(serialized_users.data)

from .seralizers import UserVerificationSerializer
@swagger_auto_schema(methods=['put'],request_body=UserVerificationSerializer)
@api_view(['PUT'])
def verify_user_by_id(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response("User does not exist", status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'PUT':
        serializer = UserVerificationSerializer(data=request.data)
        if serializer.is_valid():
            annual_salary = serializer.validated_data['annual_salary']

            if annual_salary is not None:
                user.annual_salary = annual_salary
            user.verified = True
            user.save()
            return Response("User verified successfully", status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from .models import LeaveManagement
from .seralizers import LeaveManagementSerializer
from django.utils import timezone
@swagger_auto_schema(methods=['post'],request_body=LeaveManagementSerializer)
@api_view(['POST'])
def leave_apply(request):
    if request.method == 'POST':
        serializer = LeaveManagementSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            date = serializer.validated_data['date']
         
            if not user.verified:
                return Response({"error": "User is not verified."}, status=status.HTTP_400_BAD_REQUEST)
            #remaining_leaves = leave.objects.filter(user=user, remaining__gt=0).exists()
            if user.leaves<=0:
                return Response({"error": "User has no leaves remaining."}, status=status.HTTP_400_BAD_REQUEST)

            if date < timezone.now().date():
                return Response({"error": "Leave date should be in the future."}, status=status.HTTP_400_BAD_REQUEST)

            # Check if leave already exists for the given date
            existing_leave = LeaveManagement.objects.filter(date=date,user=user).exists()
            if existing_leave:
                return Response({"error": "Leave already applied for this date."}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response("Leave applied successfully!", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



from .seralizers import LeaveManagementSerializerGet
@swagger_auto_schema(methods=['get'])
@api_view(['GET'])
def get_pending_leave_management(request):
    if request.method == 'GET':
        pending_leaves = LeaveManagement.objects.filter(status='pending')
        serializer = LeaveManagementSerializerGet(pending_leaves, many=True)
        return Response(serializer.data)
    

@swagger_auto_schema(methods=['get'])
@api_view(['GET'])
def get_approved_leave_management(request):
    approved_leaves = LeaveManagement.objects.filter(status='approved')
    serializer = LeaveManagementSerializerGet(approved_leaves, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@swagger_auto_schema(methods=['get'])
@api_view(['GET'])
def get_rejected_leave_management(request):
    rejected_leaves = LeaveManagement.objects.filter(status='rejected')
    serializer = LeaveManagementSerializerGet(rejected_leaves, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

def send_leave_email(user_email, status_recieved):
    subject = f'Leave Request {status_recieved}'
    message = f'Your Leave Request have been {status_recieved}! Thank You for your patience.'
    from_mail ='nkale882@gmail.com'
    html_message = f"""
    <!Doctype html>
    <html lang ="en">
    <head>
        <meta charset = "UTF-8">
        <title> Leave Request {status_recieved} </title>
    
    </head>
    <body>
        <h1> Your Leave Request has been {status_recieved}! </h1>
        <p>Thank You for your patience.</p>
    </body>
    </html>
    """
    send_mail(subject, message, from_mail, [user_email], html_message = html_message)
    return Response({'message': 'Email sent'}, status=status.HTTP_200_OK)
from .seralizers import UpdateLeaveStatusSerializer
@swagger_auto_schema(methods=['put'],request_body=UpdateLeaveStatusSerializer)
@api_view(['PUT'])
def update_leave_status(request, id):
    try:
        leave = LeaveManagement.objects.get(id=id)
    except LeaveManagement.DoesNotExist:
        return Response({"error": "Leave not found."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = UpdateLeaveStatusSerializer(data=request.data)
        if serializer.is_valid():
            status_value = serializer.validated_data['status']
            user = leave.user
            if status_value == UpdateLeaveStatusSerializer.APPROVED:
                if user.leaves > 0:
                    user.leaves -= 1
                    user.save()
                else:
                    return Response({"error": "User has no leaves left."}, status=status.HTTP_400_BAD_REQUEST)
            leave.status = status_value
            leave.save()
            send_leave_email(user.email,status_value)
            return Response(f"Leave {status_value} successfully!", status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

from .models import Loss_of_pay_leaveLeaveManagement
from .seralizers import LossOfPayLeaveManagementSerializer
@swagger_auto_schema(methods=['post'],request_body=LossOfPayLeaveManagementSerializer)
@api_view(['POST'])
def loss_of_pay_apply(request):
    if request.method == 'POST':
        serializer = LossOfPayLeaveManagementSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            date = serializer.validated_data['date']

           # regular_leaves_remaining =leave.objects.filter(user=user, remaining__gt=0).exists()
            if user.leaves>0:
                return Response({"error": "User has regular leaves remaining. Cannot apply for loss-of-pay leave."}, status=status.HTTP_400_BAD_REQUEST)

            # Check if leave already exists for the given date
            existing_leave = Loss_of_pay_leaveLeaveManagement.objects.filter(date=date, user=user).exists()
            if existing_leave:
                return Response({"error": "Leave already applied for this date."}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response("Loss-of-pay leave applied successfully!", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
from . seralizers import Loss_of_pay_LeaveManagementSerializerGet
@swagger_auto_schema(methods=['get'])
@api_view(['GET'])
def get_pending_loss_of_pay_leave_management(request):
        pending_leaves = Loss_of_pay_leaveLeaveManagement.objects.filter(status='pending')
        serializer = Loss_of_pay_LeaveManagementSerializerGet(pending_leaves, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    

@swagger_auto_schema(methods=['get'])
@api_view(['GET'])
def get_approved_loss_of_pay_leave_management(request):
    approved_leaves = Loss_of_pay_leaveLeaveManagement.objects.filter(status='approved')
    serializer = Loss_of_pay_LeaveManagementSerializerGet(approved_leaves, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@swagger_auto_schema(methods=['get'])
@api_view(['GET'])
def get_rejected__loss_of_pay_leave_management(request):
    rejected_leaves = Loss_of_pay_leaveLeaveManagement.objects.filter(status='rejected')
    serializer = Loss_of_pay_LeaveManagementSerializerGet(rejected_leaves, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

from .seralizers import Update_loss_of_pay_LeaveStatusSerializer
@swagger_auto_schema(methods=['put'],request_body=Update_loss_of_pay_LeaveStatusSerializer)
@api_view(['PUT'])
def update_loss_of_pay_leave_status(request, id):
    try:
        leave = Loss_of_pay_leaveLeaveManagement.objects.get(id=id)
    except Loss_of_pay_leaveLeaveManagement.DoesNotExist:
        return Response({"error": "Leave not found."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = Update_loss_of_pay_LeaveStatusSerializer(data=request.data)
        if serializer.is_valid():
            status_value = serializer.validated_data['status']
            if status_value == Update_loss_of_pay_LeaveStatusSerializer.APPROVED:
                user = leave.user
                user.leaves -= 1
                user.save()
            leave.status = status_value
            leave.save()
            return Response(f"Leave {status_value} successfully!", status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

from .seralizers import UserAnnualSalaryRevisionSerializer
@swagger_auto_schema(methods=['put'],request_body=UserAnnualSalaryRevisionSerializer)
@api_view(['PUT'])
def user_annual_salary_revision(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    if not user.verified:
        return Response({"error": "User is not verified."}, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == 'PUT':
        serializer = UserAnnualSalaryRevisionSerializer(instance=user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("User annual salary updated successfully!", status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
from .models import PayrollManagement

from .seralizers import PayrollManagementSerializer
@api_view(['GET'])
def payroll_management_list(request):
    if request.method == 'GET':
        payroll_management = PayrollManagement.objects.all()
        serializer = PayrollManagementSerializer(payroll_management, many=True)
        return Response(serializer.data)



from .seralizers import PayrollCalculationSerializer
@swagger_auto_schema(methods=['post'],request_body=PayrollCalculationSerializer)
@api_view(['POST'])
def payroll_calculation(request):
    serializer = PayrollCalculationSerializer(data=request.data)
    if serializer.is_valid():
        user= serializer.validated_data['user']
        year = serializer.validated_data['year']
        month = serializer.validated_data['month']
        user_id=user.id
        # Validate user
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        if not user.verified:
            return Response({"error": "User is not verified."}, status=status.HTTP_401_UNAUTHORIZED)

        # Check if year and month are not in the future
        current_year = datetime.date.today().year
        current_month = datetime.date.today().month

        if year > current_year or (year == current_year and month > current_month):
            return Response({"error": "Cannot calculate for future year or month."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if payroll already exists for the same user, year, and month
        if PayrollManagement.objects.filter(user=user, year=year, month=month).exists():
            return Response({"error": "Payroll already calculated for this user, year, and month."}, status=status.HTTP_400_BAD_REQUEST)

        # Perform calculations
        annual_salary = user.annual_salary
        gross_salary = annual_salary / 12  # Assuming annual salary is divided equally for each month
        provident_fund = gross_salary * 0.04
        if gross_salary <= 7500:
            professional_tax = 0
        elif 7501 <= gross_salary <= 10000:
            professional_tax = 175
        else:
            professional_tax = 200

        days_in_month = calendar.monthrange(year, month)[1]
        
        loss_of_pay =0
        if user.leaves<=-1:
            loss_of_pay = ((gross_salary - provident_fund - professional_tax) / days_in_month )* user.leaves

        net_salary = gross_salary - provident_fund - professional_tax + loss_of_pay
        
        # Save payroll data
        payroll_data = {
            'user': user_id,
            'year': year,
            'month': month,
            'gross_salary': gross_salary,
            'provident_fund': provident_fund,
            'professional_tax': professional_tax,
            'loss_of_pay': loss_of_pay,
            'net_salary': net_salary,
        }
       


        payroll_serializer = PayrollManagementSerializer(data=payroll_data)
        if payroll_serializer.is_valid():
            payroll_serializer.save()
            return Response("Payroll calculated successfully!", status=status.HTTP_201_CREATED)
        else:
            return Response(payroll_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)