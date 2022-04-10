from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView
from django.db.models import Q
from transactions.models import Transactions
from .serializers import TransactionCreateSerializer

class TransactionOrderSearchView(generics.ListAPIView):
    lookup_field = 'pk'
    queryset = Transactions.objects.all()
    serializer_class = TransactionCreateSerializer
    
    def get_queryset(self):
        qs = Transactions.objects.all()
        query = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(Q(order_id=query))
        return qs

class TransactionCustomerSearchView(generics.ListAPIView):
    lookup_field = 'pk'
    queryset = Transactions.objects.all()
    serializer_class = TransactionCreateSerializer
    
    def get_queryset(self):
        qs = Transactions.objects.all()
        query = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(Q(customer_id=query))
        return qs

class TransactionListView(generics.ListAPIView):
    lookup_field = 'pk'
    queryset = Transactions.objects.all()
    serializer_class = TransactionCreateSerializer

class TransactionRUDView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    queryset = Transactions.objects.all()
    serializer_class = TransactionCreateSerializer

class TransactionCreateView(generics.CreateAPIView):
    queryset = Transactions.objects.all()
    serializer_class = TransactionCreateSerializer
    lookup_field = 'pk'
    # permission_classes = []

class TransactionUpdateView(generics.UpdateAPIView):
    queryset = Transactions.objects.all()
    serializer_class = TransactionCreateSerializer
    lookup_field = 'pk'
    # permission_classes = []

class TransactionDeleteView(generics.DestroyAPIView):
    queryset = Transactions.objects.all()
    serializer_class = TransactionCreateSerializer
    lookup_field = 'pk'


