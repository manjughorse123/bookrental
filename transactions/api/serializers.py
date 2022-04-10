from rest_framework import serializers
from transactions.models import Transactions

class TransactionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = ('transaction', 'order', 'customer', 'status', 'transaction_date')
