from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView
from django.db.models import Q
from orders.models import OrderAddress
from .serializers import CartCreateSerializer

class CartSearchView(generics.ListAPIView):
    lookup_field = 'pk'
    queryset = OrderAddress.objects.all()
    serializer_class = CartCreateSerializer
    
    def get_queryset(self):
        qs = OrderAddress.objects.all()
        query = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(Q(customer_id=query))
        return qs

class CartListView(generics.ListAPIView):
    lookup_field = 'pk'
    queryset = OrderAddress.objects.all()
    serializer_class = CartCreateSerializer

class CartRUDView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    queryset = OrderAddress.objects.all()
    serializer_class = CartCreateSerializer

class CartCreateView(generics.CreateAPIView):
    queryset = OrderAddress.objects.all()
    serializer_class = CartCreateSerializer
    lookup_field = 'pk'
    # permission_classes = []

class CartUpdateView(generics.UpdateAPIView):
    queryset = OrderAddress.objects.all()
    serializer_class = CartCreateSerializer
    lookup_field = 'pk'
    # permission_classes = []

class CartDeleteView(generics.DestroyAPIView):
    queryset = OrderAddress.objects.all()
    serializer_class = CartCreateSerializer
    lookup_field = 'pk'
