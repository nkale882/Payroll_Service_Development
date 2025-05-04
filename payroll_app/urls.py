from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet,user_detail,user_list
from .views import EmployerViewSet, employer_detail,employer_list
from .views import user_login,employer_login
from .views import user_signup,employer_signup, update_loss_of_pay_leave_status
from .views import get_unverified_users,get_verified_users,verify_user_by_id, update_leave_status,loss_of_pay_apply
from .views import leave_apply,get_pending_leave_management, get_approved_leave_management,get_rejected_leave_management
from . views import PositionViewSet,position_list,position_detail
from .views import get_approved_loss_of_pay_leave_management,get_pending_loss_of_pay_leave_management,get_rejected__loss_of_pay_leave_management
from .views import user_annual_salary_revision, payroll_calculation,payroll_management_list


router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'employers', EmployerViewSet)
router.register(r'positions',PositionViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('users-apis/', user_list),
    path('users-apis/<int:pk>/', user_detail),
    path('employer-apis/', employer_list),
    path('employer-apis/<int:pk>/', employer_detail),
    path('api/user/signup/', user_signup, name='user-signup'),
    path('api/employer/signup/', employer_signup, name='employer-signup'),
    path('api/user/login/', user_login, name='user-login'),
    path('api/employer/login/', employer_login, name='employer-login'),
    path('employer/verified-users/', get_verified_users, name='get_verified_users'),
    path('employer/unverified-users/', get_unverified_users, name='get_unverified_users'),
    path('employer/verify-users-by-id/<int:user_id>/', verify_user_by_id, name='verify_user_by_id'),
    path('user/leave/apply/', leave_apply, name='leave-apply'),
    path('user/loss-of-pay-apply/',loss_of_pay_apply, name='loss_of_pay_apply'),
    path('employer/leave-management/pending/', get_pending_leave_management, name='get-pending-leave-management'),
    path('employer/leave-management/approved/', get_approved_leave_management, name='get_approved_leave_management'),
    path('employer/leave-management/rejected/', get_rejected_leave_management, name='get_rejected_leave_management'),
    path('employer/leave-management/update-status/<int:id>/', update_leave_status, name='update-leave-status'),
    path('positions-apis/', position_list),
    path('positions-apis/<int:pk>/', position_detail),
    path('employer/loss_of_pay-pending-leaves/', get_pending_loss_of_pay_leave_management, name='pending-leaves'),
    path('employer/loss_of_pay-approved-leaves/', get_approved_loss_of_pay_leave_management, name='approved-leaves'),
    path('employer/loss_of_pay-rejected-leaves/', get_rejected__loss_of_pay_leave_management, name='rejected-leaves'),
    path('employer/loss_of_pay_leave-management/update-status/<int:id>/', update_loss_of_pay_leave_status, name='update-loss-of-pay-leave-status'),
    path('payroll_management/user_annual_salary_revision/<int:user_id>/',user_annual_salary_revision, name='user_annual_salary_revision'),
    path('payroll_management//payroll_calculation/',payroll_calculation, name='payroll_calculation'),
    path('payroll_management/', payroll_management_list, name='payroll_management_list'),

    ]


urlpatterns += router.urls
