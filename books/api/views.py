from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView
from django.db.models import Q
from books.models import Books
from .serializers import BooksSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny

class BooksSearchView(generics.ListAPIView):
    lookup_field = 'pk'
    queryset = Books.objects.all()
    serializer_class = BooksSerializer
    
    # permission_classes = []

    def get_queryset(self):
        qs = Books.objects.all()
        query = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(Q(isbn_code=query)|Q(author_id__name__icontains=query))
        return qs

class BooksListView(generics.ListAPIView):
    lookup_field = 'pk'
    queryset = Books.objects.all()
    serializer_class = BooksSerializer    
    # permission_classes = []

class BooksPostView(generics.CreateAPIView):
    queryset = Books.objects.all()
    serializer_class = BooksSerializer
    lookup_field = 'pk'
    # permission_classes = []

class BooksRUDView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    queryset = Books.objects.all()
    serializer_class = BooksSerializer    
    # permission_classes = []

class BooksUpdateView(generics.UpdateAPIView):
    queryset = Books.objects.all()
    serializer_class = BooksSerializer
    lookup_field = 'pk'
    # permission_classes = []

class BooksDeleteView(generics.DestroyAPIView):
    queryset = Books.objects.all()
    serializer_class = BooksSerializer
    lookup_field = 'pk'
    # permission_classes = []


