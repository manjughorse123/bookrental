from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView
from django.db.models import Q
from orders.models import OrderAddress
from .serializers import OrderCreateSerializer

class OrderSearchView(generics.ListAPIView):
    lookup_field = 'pk'
    queryset = OrderAddress.objects.all()
    serializer_class = OrderCreateSerializer
    
    def get_queryset(self):
        qs = OrderAddress.objects.all()
        query = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(Q(customer_id=query))
        return qs

class OrderListView(generics.ListAPIView):
    lookup_field = 'pk'
    queryset = OrderAddress.objects.all()
    serializer_class = OrderCreateSerializer

class OrderRUDView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    queryset = OrderAddress.objects.all()
    serializer_class = OrderCreateSerializer

class OrderCreateView(generics.CreateAPIView):
    queryset = OrderAddress.objects.all()
    serializer_class = OrderCreateSerializer
    lookup_field = 'pk'
    # permission_classes = []

class OrderUpdateView(generics.UpdateAPIView):
    queryset = OrderAddress.objects.all()
    serializer_class = OrderCreateSerializer
    lookup_field = 'pk'
    # permission_classes = []

class OrderDeleteView(generics.DestroyAPIView):
    queryset = OrderAddress.objects.all()
    serializer_class = OrderCreateSerializer
    lookup_field = 'pk'


