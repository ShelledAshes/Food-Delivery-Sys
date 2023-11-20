from django.shortcuts import render
from rest_framework import status, viewsets, filters, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, AllowAny
from core.models import *
from core.serializers import *
from rest_framework.response import Response
from rest_framework import generics, status, viewsets, views
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime, timedelta
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, renderer_classes
from django.utils import timezone

def sendEmail(email, header, body):
    send_mail(
                header,
                body,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )


class OrderViewset(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (AllowAny, )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        order = Order.objects.get(id=serializer.data.get('id'))
        order.generate_otp()

        self.update_customer_detail(serializer.data, order)

        sendEmail(
            order.customer.email,
            f"Your Order {order} has been created",
            f"Here is your otp {order.otp}"
                )

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def update_customer_detail(self, data, order):
        email = data.get('customer_email')
        name = data.get('customer_name')
        try:
            customer = Customer.objects.get(email=email)
        except Customer.DoesNotExist:
            customer = Customer.objects.create(email=email, name=name)

        order.customer = customer
        order.save()

class FoodProductViewset(viewsets.ModelViewSet):
    queryset = FoodProduct.objects.all()
    serializer_class = FoodProductSerializer
    permission_classes = (AllowAny, )


class CustomerViewset(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = (AllowAny, )


class DeliveryAgentViewset(viewsets.ModelViewSet):
    queryset = DeliveryAgent.objects.all()
    serializer_class = DeliveryAgentSerializer
    permission_classes = (AllowAny, )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        delivery_agent = DeliveryAgent.objects.get(id=serializer.data.get('id'))
        delivery_agent.generate_password()

        sendEmail(
            delivery_agent.email,
            "Welcome to Food Delivery System",
            f"Your username: {delivery_agent.email}\nYour password: {delivery_agent.password}"
            )
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers) 

 
class DeliveryAgentOrdersView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = (AllowAny, )

    def get_queryset(self):
        orders = Order.objects.filter(delivery_agent=self.kwargs.get('pk'))
        return orders 


class CustomerOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = (AllowAny, )

    def get_queryset(self):
        orders = Order.objects.filter(customer=self.kwargs.get('pk'))
        return orders 
    

class UpdateOrderStatusView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (AllowAny, )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        otp = request.data.get('otp')
        order_status = request.data.get('status')

        if order_status == "DELIVERED":
            if otp != instance.otp:
                return Response({'message': 'Please enter the correct OTP'}, status=status.HTTP_400_BAD_REQUEST)
            instance.status = order_status
            instance.save()
            return Response({'message': 'Your order delivery confirmed.'}, status=status.HTTP_200_OK)    
        
        if order_status == "CANCELLED":
            instance.cancel_order()
            sendEmail(
                instance.customer.email,
                f"Your Order {instance} has been cancelled",
                f""
                  )
            return Response({'message': 'Your order has been cancelled.'}, status=status.HTTP_200_OK)    


@api_view(['GET'])
@renderer_classes([JSONRenderer])      
def cancel_order(request, pk):    
    order = Order.objects.get(id=pk)
    time_diff = datetime.now(timezone.utc) - order.created_at
    if time_diff <= timedelta(minutes=30):
        order.cancel_order()
        sendEmail(
            order.customer.email,
            f"Your Order {order} has been cancelled",
            f""
                )
        
        return Response({'message': 'Order cancelled successfully.'}, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Cancellation time exceeded.'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@renderer_classes([JSONRenderer])    
def soft_delete_profile(request, pk):    
    customer = Customer.objects.get(id=pk)
    orders = Order.objects.filter(customer=customer, status="PENDING")

    if len(orders) == 0:
        customer.softly_delete()
        return Response({'message': 'Profile soft deletion successfull.'}, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Profile soft deletion unsuccessfull, still orders pending.'}, status=status.HTTP_200_OK)
    


