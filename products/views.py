# products/views.py

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Category, Subcategory, Product, Country, Like, ProductView, Comment, Favorite
from .serializers import (CategorySerializer, SubcategorySerializer,
                          ProductSerializer, CountrySerializer,
                          LikeSerializer, CommentSerializer, ProductViewSerializer, FavoriteSerializer)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class SubcategoryViewSet(viewsets.ModelViewSet):
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'subcategory', 'condition', 'country_of_origin']
    search_fields = ['name']
    ordering_fields = ['price']

    # Swagger-аннотация для фильтров
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('category', openapi.IN_QUERY, description="ID категории", type=openapi.TYPE_INTEGER),
            openapi.Parameter('subcategory', openapi.IN_QUERY, description="ID подкатегории", type=openapi.TYPE_INTEGER),
            openapi.Parameter('condition', openapi.IN_QUERY, description="Состояние продукта (new, used, refurbished)", type=openapi.TYPE_STRING),
            openapi.Parameter('price_min', openapi.IN_QUERY, description="Минимальная цена", type=openapi.TYPE_NUMBER),
            openapi.Parameter('price_max', openapi.IN_QUERY, description="Максимальная цена", type=openapi.TYPE_NUMBER),
            openapi.Parameter('country_of_origin', openapi.IN_QUERY, description="Страна происхождения", type=openapi.TYPE_INTEGER),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # Метод для увеличения просмотров
    @action(detail=True, methods=['get'])
    def view_product(self, request, pk=None):
        product = self.get_object()
        product.views += 1
        product.save()
        serializer = self.get_serializer(product)
        return Response(serializer.data)

    # Дополнительный метод для получения ссылки "поделиться"
    @action(detail=True, methods=['get'])
    def share(self, request, pk=None):
        product = self.get_object()
        share_url = f"http://yourdomain.com/products/{product.id}/"
        return Response({"share_url": share_url})


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class ProductViewViewSet(viewsets.ModelViewSet):
    queryset = ProductView.objects.all()
    serializer_class = ProductViewSerializer

class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
