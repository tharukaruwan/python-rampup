from django.urls import path
from customerApp import views

urlpatterns=[
    path('customers',views.apiCustomers,name='api-customers'),
    path('customer/login',views.apiCustomerLogin,name='api-customer-login'),
    path('customers/<str:id>',views.apiCustomer,name='api-customer'),

    path('orders',views.apiOrders,name='api-orders'),
    path('orders/<int:id>',views.apiOrder,name='api-order'),
]