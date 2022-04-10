from rest_framework import serializers
from suppliers.models import Suppliers,Shop

class SuppliersListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suppliers
        fields = ('user_id', 'wallet_id', 'address1', 'city', 'postal_code')

class SuppliersGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suppliers
        fields = '__all__'

class SuppliersCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suppliers
        fields = '__all__'

class SuppliersUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suppliers
        fields = '__all__'

class SuppliersDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suppliers
        fields = '__all__'

class ShopListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ('id', 'owner_id', 'name', 'address', 'city', 'phone_number')

class ShopGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ('id', 'owner_id', 'name', 'address', 'city', 'phone_number')

class ShopCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ('id', 'owner_id', 'name', 'address', 'city', 'phone_number')

class ShopUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ('id', 'owner_id', 'name', 'address', 'city', 'phone_number')

class ShopDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ('id', 'owner_id', 'name', 'address', 'city', 'phone_number')
