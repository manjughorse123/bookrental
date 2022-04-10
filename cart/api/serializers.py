from rest_framework import serializers
from orders.models import OrderAddress

CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderAddress
        fields = '__all__'
    