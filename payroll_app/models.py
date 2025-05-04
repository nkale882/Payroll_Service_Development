from django.db import models

class Position(models.Model):
    Position = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'position' 

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number= models.BigIntegerField()
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    verified=models.BooleanField(default=False)
    created_date= models.DateTimeField(auto_now_add=True)
    modified_date= models.DateTimeField(auto_now=True)
    position= models.ForeignKey(Position,on_delete=models.SET_NULL,null=True,blank=True)
    leaves= models.IntegerField(default=10)
    annual_salary = models.IntegerField( null=True, blank=True)

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'user'

class Employer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number= models.BigIntegerField()
    email = models.EmailField()
    password = models.CharField(max_length=100)
    created_date= models.DateTimeField(auto_now_add=True)
    modified_date= models.DateTimeField(auto_now=True)

    def __str__(self):
         return self.email
    
    class Meta:
        db_table = 'Employer'

from django.utils.translation import gettext_lazy as _

class LeaveManagement(models.Model):
    STATUS_CHOICES = [
        ('pending', ('Pending')),
        ('approved', ('Approved')),
        ('rejected', ('Rejected')),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.user}"

    class Meta:
       db_table= 'Leave Management'

class Loss_of_pay_leaveLeaveManagement(models.Model):
    STATUS_CHOICES = [
        ('pending', ('Pending')),
        ('approved', ('Approved')),
        ('rejected', ('Rejected')),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.user}"

    class Meta:
       db_table= 'loss-of-pay-LeaveManagement'


from django.utils import timezone

class PayrollManagement(models.Model):
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

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    year = models.IntegerField(choices=[(year, year) for year in range(1984, timezone.now().year + 1)])
    month = models.IntegerField(choices=MONTH_CHOICES)
    gross_salary = models.FloatField(null=True,blank=True)
    provident_fund = models.FloatField(null=True,blank=True)
    professional_tax = models.FloatField(null=True,blank=True)
    loss_of_pay = models.FloatField(default=0.00)
    net_salary = models.FloatField(null=True,blank=True)

    def __str__(self):
        return f"{self.user}"

    class Meta:
       db_table= 'payroll-management'