from django.urls import path

from rest_framework.routers import SimpleRouter
from core.views import *


router = SimpleRouter()
router.register(r'delivery-agents', DeliveryAgentViewset)
router.register(r'customers', CustomerViewset)
router.register(r'food-products', FoodProductViewset)
router.register(r'orders', OrderViewset)
router.register(r'delivery-orders', OrderViewset)

urlpatterns = [
    path('delivery_agent/orders/<int:pk>/', DeliveryAgentOrdersView.as_view()),
    path('delivery_agent/update_order_status/<int:pk>/', UpdateOrderStatusView.as_view()),
    path('customer/order-list/<int:pk>/', CustomerOrderListView.as_view()),
    path('customer/cancel-order/<int:pk>/', cancel_order),
    path('customer/soft-delete-profile/<int:pk>/', soft_delete_profile),
    path('email/', sendEmail),
] + router.urls
