from django.urls import path
from rest_framework import routers
from ecom import views
from ecom.views import MessageViewSet  # ✅ Import
from ecom.views import MessageViewSet, clear_cart  # ✅ Proper import

# ✅ Router registration
router = routers.DefaultRouter()
router.register(r'units', views.UnitModelViewSet, basename='unit')
router.register(r'product', views.ProductModelViewSet, basename='product')
router.register(r'category', views.CategoryModelViewSet, basename='category')
router.register(r'orders', views.OrderViewSet, basename='orders')  # ✅ Add this
router.register(r'messages', MessageViewSet, basename='messages')



# ✅ Custom URL patterns
urlpatterns = [
    path('add_to_cart/', views.AddToCart.as_view(), name='add_to_cart'),
    path('update_cart/', views.UpdateCart.as_view(), name='update_cart'),
    path('remove_cart_item/<int:id>/', views.DeleteCartItem.as_view(), name='remove_cart_item'),
    path('pay_bill/', views.PayBill.as_view(), name='pay_bill'),

    path('get_product_count/', views.get_product_count, name='get_product_count'),

    path('get_total_orders/', views.get_total_orders, name='get_total_orders'),
    path('get_completed_orders/', views.get_completed_orders, name='get_completed_orders'),
    path('get_pending_orders/', views.get_pending_orders, name='get_pending_orders'),
    path('get_total_product_count/', views.get_total_product_count, name='get_total_product_count'),
    path('place_order/', views.place_order, name='place_order'),
    path('clear_cart/', clear_cart),



] 

# ✅ Append DRF router URLs
urlpatterns += router.urls
