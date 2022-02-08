from dataclasses import field
from pyexpat import model
from rest_framework import serializers
from customerApp.models import Customer, CustomerOrder

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Customer
        fields='__all__'
        # fields=('email','firstName','lastName','dateOfBirth','currencyBalance','pageVisitors')

class CustomerOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomerOrder
        fields='__all__'
        