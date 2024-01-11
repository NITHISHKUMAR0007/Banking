from django.urls import path
from . import views

urlpatterns=[
    path('',views.index,name='index'),
    path('login',views.login,name='login'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('register',views.register,name='register'),
    path('register_form_submission',views.register_form_submission,name='register_form_submission'),
    path('login_form_submission',views.login_form_submission,name='login_form_submission'),
    path('deposit_amount_stored/<str:account_number>',views.deposit_amount_stored,name='deposit_amount_stored'),
    path('withdraw_amount_stored/<str:account_number>',views.withdraw_amount_stored,name='withdraw_amount_stored'),
    path('PBI_all_registered_users/',views.PBI_register_List.as_view()),
]
