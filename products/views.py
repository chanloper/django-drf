from django.core.cache import cache
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response


from . models import Product
from .serializers import ProductSerializer


# 함수형 뷰를 사용할 땐 api_view를 달아줘야 한다.
@api_view(["GET"])
def product_list(request):
    cache_key = "product_list"
    if not cache.get(cache_key):
        print("cache Miss")
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        json_response = serializer.data
        cache.set("product_list", json_response, 5)

    response_data = cache.get(cache_key)
    return Response(response_data)
