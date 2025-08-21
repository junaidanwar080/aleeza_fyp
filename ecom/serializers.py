from rest_framework import serializers
from .models import Message
from ecom.models import (
    Category,
    Products,
    Units,
    StockSaleMain,
    StockSaleDetail,
    Order,
    OrderItem
)

# --------------------------
# Unit Serializer
# --------------------------
class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Units
        fields = "__all__"


# --------------------------
# Category Serializer
# --------------------------
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


# --------------------------
# Product Serializer
# --------------------------
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = "__all__"


# --------------------------
# Stock Sale Detail Serializer
# --------------------------
class StockSaleDetailSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_image = serializers.ImageField(source='product.image', read_only=True)
    product = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = StockSaleDetail
        fields = [
            'id', 'product', 'product_name', 'product_image',
            'quantity', 'price', 'total_price'
        ]

    def get_total_price(self, obj):
        return float(obj.quantity) * float(obj.price) if obj.quantity and obj.price else 0


# --------------------------
# OrderItem Serializer
# --------------------------
class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField(read_only=True)
    product_code = serializers.SerializerMethodField(read_only=True)
    product_image = serializers.SerializerMethodField(read_only=True)
    unit_price = serializers.DecimalField(
        source='sale_price', max_digits=10, decimal_places=2
    )
    subtotal = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            'product',
            'product_name',
            'product_code',
            'product_image',
            'quantity',
            'unit_price',
            'subtotal'  # ✅ Add this line
        ]

    def get_product_name(self, obj):
        return obj.product.name if obj.product else obj.name

    def get_product_code(self, obj):
        return obj.product.code if obj.product else ""

    def get_product_image(self, obj):
        return obj.product.image.url if obj.product and obj.product.image else ""

    def get_subtotal(self, obj):
        return float(obj.quantity) * float(obj.sale_price)



# --------------------------
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            'id', 'first_name', 'last_name', 'email',
            'address1', 'phone', 'country', 'state', 'zip_code',
            'shipping', 'total_amount', 'created_at', 'items'
        ]

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)

        for item in items_data:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                sale_price=item['sale_price']
            )

        return order





# --------------------------
# Message Serializer
# --------------------------
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
