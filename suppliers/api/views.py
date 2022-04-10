from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView
from django.db.models import Q
from suppliers.models import Suppliers
from books.models import Books
from .serializers import *
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny

class SuppliersSearchView(generics.ListAPIView):
    serializer_class = SuppliersListSerializer
    queryset = Suppliers.objects.all()
    lookup_field = 'pk'    
    # permission_classes = []

    def get_queryset(self):
        qs = Suppliers.objects.all()
        query = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(Q(user_id__id__icontains=query)|Q(user_id__user_role__icontains=query))
        return qs

class SuppliersListView(generics.ListAPIView):
    serializer_class = SuppliersListSerializer
    queryset = Suppliers.objects.all()
    lookup_field = 'pk'    
    # permission_classes = []   

class SuppliersCreateView(generics.CreateAPIView):
    serializer_class = SuppliersCreateSerializer
    queryset = Suppliers.objects.all()
    lookup_field = 'pk'
    # permission_classes = []

class SuppliersRUDView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SuppliersGetSerializer    
    queryset = Suppliers.objects.all()    
    lookup_field = 'pk'
    # permission_classes = []

class SuppliersUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = SuppliersUpdateSerializer
    queryset = Suppliers.objects.all()
    lookup_field = 'pk'
    # permission_classes = []

class SuppliersDeleteView(generics.RetrieveDestroyAPIView):
    serializer_class = SuppliersDeleteSerializer
    queryset = Suppliers.objects.all()
    lookup_field = 'pk'
    # permission_classes = []



class ShopSearchId(generics.ListAPIView):
    serializer_class = ShopListSerializer
    queryset = Shop.objects.all()
    lookup_field = 'pk'    
    # permission_classes = []

    def get_queryset(self):
        qs = Shop.objects.all()
        query = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(Q(id=query))
        return qs

class ShopSearchOwner(generics.ListAPIView):
    serializer_class = ShopListSerializer
    queryset = Shop.objects.all()
    lookup_field = 'pk'    
    # permission_classes = []

    def get_queryset(self):
        qs = Shop.objects.all()
        query = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(Q(owner_id=query))
        return qs


class ShopListView(generics.ListAPIView):
    serializer_class = ShopListSerializer
    queryset = Shop.objects.all()
    lookup_field = 'pk'    
    # permission_classes = []

class ShopCreateView(generics.CreateAPIView):
    serializer_class = ShopCreateSerializer
    queryset = Shop.objects.all()
    lookup_field = 'pk'
    # permission_classes = []

class ShopRUDView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ShopGetSerializer    
    queryset = Shop.objects.all()    
    lookup_field = 'pk'
    # permission_classes = []

class ShopUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = ShopUpdateSerializer
    queryset = Shop.objects.all()
    lookup_field = 'pk'
    # permission_classes = []

class ShopDeleteView(generics.RetrieveDestroyAPIView):
    serializer_class = ShopDeleteSerializer
    queryset = Shop.objects.all()
    lookup_field = 'pk'
    # permission_classes = []

# class SuppliersListView(APIView):
#     """
#     List all Supplierss, or create a new Suppliers.
#     """
#     def get(self, request, format=None):
#         suppliers = Suppliers.objects.all()
#         serializer = SuppliersListSerializer(suppliers, many=True)
#         return Response(serializer.data)

#     def post(self, request, format=None):
#         serializer = SuppliersListSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class SuppliersRUDView(APIView):
#     """
#     Retrieve, update or delete a Suppliers instance.
#     """
#     def get_object(self, pk):
#         try:
#             return Suppliers.objects.get(pk=pk)
#         except Suppliers.DoesNotExist:
#             raise Http404

#     def get(self, request, pk, format=None):
#         suppliers = self.get_object(pk)
#         serializer = SuppliersListSerializer(suppliers)
#         return Response(serializer.data)

#     def put(self, request, pk, format=None):
#         suppliers = self.get_object(pk)
#         serializer = SuppliersListSerializer(suppliers, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk, format=None):
#         suppliers = self.get_object(pk)
#         suppliers.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)