# payroll_app/management/commands/monthly_task.py

from django.core.management.base import BaseCommand
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from django.core.mail import send_mail
import calendar

from payroll_app.models import PayrollManagement, User
from payroll_app.seralizers import PayrollManagementSerializer
from pprint import pprint
import calendar

from payroll_project.settings import EMAIL_HOST_USER


def send_payroll_email(month, year, user, monthly_salary, provident_fund, professional_tax, loss_of_pay, net_salary):
    subject = f"Your Payroll Details For Month {calendar.month_name[month]} {year}"
    message = (
        f"Hello {user.first_name}, \n\n"
        f"Your Payroll Details For the Month of {calendar.month_name[month]} {year} are as follows: \n\n"
        f"Gross Salary: {monthly_salary}\n"
        f"Provident Fund: {provident_fund}\n"
        f"Professional Tax: {professional_tax}\n"
        f"Loss Of Pay: {loss_of_pay}\n"
        f"Net Salary: {net_salary}\n\n"
        f"Thank You. \n"
    )
    
    html_message = (
        f"<p>Hello {user.first_name},</p>"
        f"<p>Your payroll details for the month of {calendar.month_name[month]} {year} are as follows: \n\n</p>"
        f"<ul>"
        f"<li>Gross Salary: {monthly_salary}</li>"
        f"<li>Provident Fund: {provident_fund}</li>"
        f"<li>Professional Tax: {professional_tax}</li>"
        f"<li>Loss of Pay: {loss_of_pay}</li>"
        f"<li>Net Salary: {net_salary}</li>"
        f"</ul>"
        f"<p>Thank you.</p>"
    )
    
    recipient_email = user.email
    send_mail(subject, message, EMAIL_HOST_USER, [recipient_email], html_message=html_message)


def monthly_task():
    current_year = datetime.now().year
    current_month = datetime.now().month
    last_month = current_month - 1 if current_month > 1 else 12
    users = User.objects.all()
    
    for user in users:
        pprint(user)
        
        year = datetime.now().year
        current_month = datetime.now().month
        month = current_month - 1 if current_month > 1 else 12
        
        if not user.verified:
            print("User Not Verified")
        else:
            existing_record = PayrollManagement.objects.filter(user=user, month=month, year=year).exists()
            if existing_record:
                print(f"User has existing record {user} {year} {month}")
            else:
                monthly_salary = user.annual_salary / 12
                provident_fund = monthly_salary * 0.04
        
                if monthly_salary <= 7500:
                    professional_tax = 0
                elif 7501 <= monthly_salary <= 10000:
                    professional_tax = 175
                else:
                    professional_tax = 200
                    
                num_days_in_month = calendar.monthrange(year, month)[1]
                net_salary = monthly_salary - provident_fund - professional_tax
                    
                pay_per_day = net_salary / num_days_in_month
                
                loss_of_pay = 0
                
                if user.leaves < 0:
                    loss_of_pay = user.leaves * pay_per_day
                    
                net_salary += loss_of_pay
    
                print('/////////////////////////////////////////////////')
                
                new_payroll_data = {
                    'user' : user.pk,
                    'year' : year,
                    'month' : month,
                    'gross_salary' : "{:.2f}".format(monthly_salary),
                    'provident_fund' : "{:.2f}".format(provident_fund),
                    'professional_tax' : "{:.2f}".format(professional_tax),
                    'loss_of_pay' : "{:.2f}".format(loss_of_pay), 
                    'net_salary' : "{:.2f}".format(net_salary),
                }
                serializer = PayrollManagementSerializer(data=new_payroll_data)
                if serializer.is_valid():
                    serializer.save()
                    send_payroll_email(month, year, user, "{:.2f}".format(monthly_salary), "{:.2f}".format(provident_fund),
                                          "{:.2f}".format(professional_tax), "{:.2f}".format(loss_of_pay),
                                          "{:.2f}".format(net_salary))
                    if loss_of_pay:
                        user.leaves = 0
                        user.save()
                else:
                    print(serializer.errors)


class Command(BaseCommand):
    help = 'Calculate payroll for the previous month and send emails'

    def handle(self, *args, **kwargs):
        scheduler = BackgroundScheduler()
        scheduler.add_job(monthly_task, 'interval', seconds=15)  # Adjust the interval as needed
        scheduler.start()

        #self.stdout.write(self.style.SUCCESS('Scheduler started. Press Ctrl+C to exit.'))

        try:
            while True:
                pass
        except (KeyboardInterrupt, SystemExit):
            scheduler.shutdown()
            #self.stdout.write(self.style.SUCCESS('Scheduler stopped.'))