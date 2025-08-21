from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone

from rest_framework.decorators import api_view
from rest_framework.response import Response
from ecom.serializers import OrderSerializer, OrderItemSerializer  # ✅ Add this
from rest_framework.decorators import permission_classes




from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

from ecom.models import Units, Category, Products, StockSaleMain, StockSaleDetail
from ecom.serializers import (
    UnitSerializer,      
    CategorySerializer,
    ProductSerializer,
    StockSaleDetailSerializer
)
  
# ✅ Units ViewSet
class UnitModelViewSet(viewsets.ModelViewSet):
    queryset = Units.objects.all()
    serializer_class = UnitSerializer 
    permission_classes = [AllowAny]


# ✅ Category ViewSet
class CategoryModelViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


# ✅ Product ViewSet
class ProductModelViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]


# ✅ Add to Cart
class AddToCart(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            last_invoice = StockSaleMain.objects.latest('invoice_no')
            if last_invoice.status == "draft":
                cart_items = StockSaleDetail.objects.filter(stock_sale_main=last_invoice.invoice_no)
                serializer = StockSaleDetailSerializer(cart_items, many=True)
                return Response({'cart_items': serializer.data})
        except StockSaleMain.DoesNotExist:
            pass

        return Response({'cart_items': []})

    def post(self, request):
        try:
            product = Products.objects.get(id=request.data.get('item_id'))
            quantity = int(request.data.get('quantity'))
            unit_price = float(request.data.get('unit_price'))
            try:
                last_invoice = StockSaleMain.objects.latest('invoice_no')
                if last_invoice.status == "draft":
                    count = StockSaleDetail.objects.filter(stock_sale_main=last_invoice.invoice_no).count()
                    
                else:
                    count = 0
            except StockSaleMain.DoesNotExist:
                count = 0
            if count == 0:
                sale_main = StockSaleMain.objects.create(invoice_date=timezone.now())
                StockSaleDetail.objects.create(
                    product=product,
                    quantity=quantity,
                    price=unit_price,
                    stock_sale_main=sale_main
                )
            else:
                self.update_cart(last_invoice.invoice_no)
            return Response({"success": True, "message": "Item added to cart successfully"})
        except Products.DoesNotExist:
            return Response({"success": False, "message": "Product not found"}, status=404)
        except Exception as e:
            return Response({"success": False, "message": str(e)}, status=500)
        
    def update_cart(self,last_invoice):
        print(last_invoice)
       
        
        try:
            product = Products.objects.get(id = self.request.data['item_id'])
            quantity = int(self.request.data['quantity'])
            unit_price = float(self.request.data['unit_price'])
            invoice_no = StockSaleMain.objects.latest('invoice_no').invoice_no
            sale_main = StockSaleMain.objects.get(invoice_no=invoice_no)

            StockSaleDetail.objects.create(
                product=product,
                quantity=quantity,
                price=unit_price,
                stock_sale_main=sale_main
            )
            response = "Cart Updated"
            return response
        except Exception as e:
            response = "something went wrong"
            print(f"Error updating cart: {str(e)}")
            return response



class UpdateCart(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        item_id = request.data.get('item_id')
        action = request.data.get('action')

        if not item_id or not action:
            return Response({"error": "item_id and action are required"}, status=400)

        try:
            product = Products.objects.get(id=item_id)
            sale_main = StockSaleMain.objects.latest('invoice_no')

            # 🔍 Get existing cart item
            cart_item = StockSaleDetail.objects.filter(product=product, stock_sale_main=sale_main).first()

            if not cart_item:
                return Response({"error": "Cart item not found"}, status=404)

            if action == 'increase':
                cart_item.quantity += 1
                cart_item.save()
                return Response({"success": "Quantity increased"}, status=200)

            elif action == 'decrease':
                cart_item.quantity -= 1
                if cart_item.quantity <= 0:
                    cart_item.delete()
                    return Response({"success": "Item removed from cart"}, status=200)
                else:
                    cart_item.save()
                    return Response({"success": "Quantity decreased"}, status=200)

            else:
                return Response({"error": "Invalid action"}, status=400)

        except Products.DoesNotExist:
            return Response({"error": "Product not found"}, status=404)
        except StockSaleMain.DoesNotExist:
            return Response({"error": "No draft invoice found"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=400)

# ✅ Delete Cart Item
class DeleteCartItem(APIView):
    permission_classes = [AllowAny]

    def delete(self, request, id):
        deleted, _ = StockSaleDetail.objects.filter(id=id).delete()
        return Response({"success": "Item removed", "deleted_count": deleted}, status=200)


# ✅ Pay Bill
class PayBill(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            invoice_no = StockSaleMain.objects.latest('invoice_no').invoice_no
            sale_main = StockSaleMain.objects.get(invoice_no=invoice_no)
            sale_main.status = "completed"
            sale_main.save()
            return Response({"success": "Bill paid successfully"})
        except StockSaleMain.DoesNotExist:
            return Response({"error": "Bill not found"}, status=404)


# ✅ Count APIs
def get_product_count(request):
    try:
        last_invoice = StockSaleMain.objects.latest('invoice_no')
        if last_invoice.status == "draft":
            count = StockSaleDetail.objects.filter(stock_sale_main=last_invoice.invoice_no).count()
        else:
            count = 0
    except StockSaleMain.DoesNotExist:
        count = 0
    return JsonResponse({'product_count': count})


def get_total_orders(request):
    count = StockSaleMain.objects.count()
    return JsonResponse({'total_orders': count})


def get_completed_orders(request):
    count = StockSaleMain.objects.filter(status='completed').count()
    return JsonResponse({'completed_orders': count})


def get_pending_orders(request):
    count = StockSaleMain.objects.filter(status='draft').count()
    return JsonResponse({'pending_orders': count})


def get_total_product_count(request):
    count = Products.objects.count()
    return JsonResponse({'product_count': count})





@api_view(['POST'])
@permission_classes([AllowAny])   # ✅ Add this line to bypass default permission

def place_order(request):
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)



from rest_framework import viewsets
from ecom.models import Order
from ecom.serializers import OrderSerializer

# ✅ Admin: View All Orders
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]  # ✅ Add this line



from ecom.models import Message  # ✅ Add import
from ecom.serializers import MessageSerializer  # ✅ Add import

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().order_by('-created_at')
    serializer_class = MessageSerializer
    permission_classes = [AllowAny]



@api_view(['DELETE'])
@permission_classes([AllowAny])
def clear_cart(request):
    try:
        last_invoice = StockSaleMain.objects.latest('invoice_no')
        if last_invoice.status == "draft":
            count, _ = StockSaleDetail.objects.filter(stock_sale_main=last_invoice).delete()
            return Response({"success": f"{count} items removed from cart"})
        return Response({"info": "No draft cart to clear"}, status=200)
    except StockSaleMain.DoesNotExist:
        return Response({"error": "No draft invoice found"}, status=404)
