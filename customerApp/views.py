import requests

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from customerApp.models import Customer
from customerApp.serializers import CustomerSerializer

from customerApp.models import CustomerOrder
from customerApp.serializers import CustomerOrderSerializer

from django.conf import settings
import firebase_admin
from firebase_admin import credentials

firebase_cred=credentials.Certificate(settings.FIREBASE_CONFIG)
firebase_app = firebase_admin.initialize_app(firebase_cred)

def NewUser(email,password):
    apikey='AIzaSyDR0KFr8_L_K9UjK--OoSA_jIhKkuyHHB8'
    details={
        'email':email,
        'password':password,
        'returnSecureToken': True
    }
    r=requests.post('https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={}'.format(apikey),data=details)
    if 'error' in r.json().keys():
        return {'status':'error','message':r.json()['error']['message']}
    if 'idToken' in r.json().keys() :
        return {'status':'success','idToken':r.json()['idToken'],'refreshToken':r.json()['refreshToken'],'id':r.json()['localId']}

def loginUser(email,password):
    apikey='AIzaSyDR0KFr8_L_K9UjK--OoSA_jIhKkuyHHB8'
    details={
        'email':email,
        'password':password,
        'returnSecureToken': True
    }
    r=requests.post('https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={}'.format(apikey),data=details)
    if 'error' in r.json().keys():
        return {'status':'error','message':r.json()['error']['message']}
    if 'idToken' in r.json().keys() :
        return {'status':'success','idToken':r.json()['idToken'],'refreshToken':r.json()['refreshToken'],'id':r.json()['localId']}

def userAuthorization(tocken,id):
    user_id=''
    try:
        user_id=tocken["user_id"]
    except:
        user_id=''
    if user_id=='' or user_id!=id:
        return False
    return True

def orderViewAuthorization(tocken,order):
    user_id=''
    try:
        user_id=tocken["user_id"]
    except:
        user_id=''
    if user_id=='' or user_id!=order["customer"]:
        return False
    return True
    

@api_view(['POST','GET' ])
def apiCustomers(request):
    # signup
    if request.method == 'POST':
        # firebase register
        user=NewUser(request.data["email"],request.data["password"])
        if user["status"]=='error':
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        request.data["customerId"]=user["id"]
        customer_serializer=CustomerSerializer(data=request.data)
        if customer_serializer.is_valid():
            customer_serializer.save()
            data={  'id':customer_serializer.data["customerId"],
                    'email':customer_serializer.data["email"],
                    'firstName':customer_serializer.data["firstName"],
                    'accessTocken':user["idToken"],
                    'refreshToken':user["refreshToken"] }
            return Response(data,status=status.HTTP_201_CREATED)
        return Response(customer_serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        customers= Customer.objects.all()
        customers_serializer=CustomerSerializer(customers,many=True)
        return Response(customers_serializer.data,status=status.HTTP_200_OK)

# Login customer
@api_view(['POST'])
def apiCustomerLogin(request):
    try:
        customer= Customer.objects.get(email=request.data["email"])
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    customer_serializer=CustomerSerializer(customer,many=False)
    user=loginUser(customer_serializer.data["email"],request.data["password"])

    data={  'id':customer_serializer.data["customerId"],
            'email':customer_serializer.data["email"],
            'firstName':customer_serializer.data["firstName"],
            'accessTocken':user["idToken"],
            'refreshToken':user["refreshToken"] }
    return Response(data,status=status.HTTP_200_OK)

# Protected route
@api_view(['GET','PUT','DELETE'])
def apiCustomer(request,id):
    # Protect route
    if userAuthorization(request.tocken,id)==False:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    try:
        customer= Customer.objects.get(customerId=id)
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        customer_serializer=CustomerSerializer(customer,many=False)
        return Response(customer_serializer.data,status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        customer_serializer=CustomerSerializer(customer,data=request.data)
        if customer_serializer.is_valid():
            customer_serializer.save()
            return Response(customer_serializer.data,status=status.HTTP_205_RESET_CONTENT)
        return Response(customer_serializer.errors,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    elif request.method == 'DELETE':
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST','GET' ])
def apiOrders(request):
    if request.method == 'POST':
        # verify 
        if request.tocken=='':
           return Response(status=status.HTTP_401_UNAUTHORIZED) 
        request.data["customer"]=request.tocken["user_id"]
        order_serializer=CustomerOrderSerializer(data=request.data)
        if order_serializer.is_valid():
            order_serializer.save()
            return Response(order_serializer.data,status=status.HTTP_201_CREATED)
        return Response(order_serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        orders= CustomerOrder.objects.all()
        print(orders)
        # return Response(status=status.HTTP_200_OK)
        orders_serializer=CustomerSerializer(orders,many=True)
        return Response(orders_serializer.data,status=status.HTTP_200_OK)

@api_view(['GET','PUT','DELETE'])
def apiOrder(request,id):
    try:
        order= CustomerOrder.objects.get(orderId=id)
    except CustomerOrder.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    order_serializer=CustomerOrderSerializer(order,many=False)
    # Protect route
    if orderViewAuthorization(request.tocken,order_serializer.data)==False:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    if request.method == 'GET':
        return Response(order_serializer.data,status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        order_serializer=CustomerOrderSerializer(order,data=request.data)
        if order_serializer.is_valid():
            order_serializer.save()
            return Response(order_serializer.data,status=status.HTTP_205_RESET_CONTENT)
        return Response(order_serializer.errors,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    elif request.method == 'DELETE':
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
