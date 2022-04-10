from rest_framework import serializers
from orders.models import OrderAddress

class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderAddress
        fields = '__all__'
