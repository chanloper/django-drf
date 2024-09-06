from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from django.shortcuts import get_object_or_404
from . models import Article, Comment
from .serializers import ArticleSerializer, ArticleDetailSerializer, CommentSerializer

# HTTPS_STATUS_201_CREATED = 201

# 함수형 View 형태

# @api_view(["GET", "POST"])
# def article_list(request):
#     if request.method == "GET":
#         articles = Article.objects.all()
#         serializer = ArticleSerializer(articles, many=True)
#         return Response(serializer.data)

#     elif request.method == "POST":
#         serializer = ArticleSerializer(data=request.data)
#         # return Response(serializer.errors, status=400)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)


# @api_view(["GET", "PUT", "DELETE"])
# def article_detail(request, pk):

#     if request.method == "GET":
#         article = get_object_or_404(Article, pk=pk)
#         serializers = ArticleSerializer(article)
#         return Response(serializers.data)

#     elif request.method == "PUT":
#         article = get_object_or_404(Article, pk=pk)
#         serializer = ArticleSerializer(article, data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response(serializer.data)

#     elif request.method == "DELETE":
#         article = get_object_or_404(Article, pk=pk)
#         article.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# 클래스형 View 형태
# from rest_framework.views import APIView 호출 필요

class ArticleListAPIView(APIView):

    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Articles"],
        description="Article 목록 조회를 위한 API",
    )
    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    @extend_schema(
        tags=["Articles"],
        description="Article 생성을 위한 API",
        request=ArticleSerializer,
    )
    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        # return Response(serializer.errors, status=400)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class ArticleDetailAPIView(APIView):

    permission_classes = [IsAuthenticated]  # 접근 제한

    def get_object(self, pk):
        return get_object_or_404(Article, pk=pk)

    def get(self, request, pk):
        article = self.get_object(pk)
        serializers = ArticleDetailSerializer(article)
        return Response(serializers.data)

    def put(self, request, pk):
        article = self.get_object(pk)
        serializer = ArticleDetailSerializer(article, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, pk):
        article = self.get_object(pk)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentListAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, article_pk):
        article = get_object_or_404(Article, pk=article_pk)
        comments = article.comments.all()
        serializers = CommentSerializer(comments, many=True)
        return Response(serializers.data)

    def post(self, request, article_pk):
        article = get_object_or_404(Article, pk=article_pk)
        serializers = CommentSerializer(data=request.data)
        if serializers.is_valid(raise_exception=True):
            serializers.save(article=article)
            return Response(serializers.data, status=status.HTTP_201_CREATED)


class CommentDetailAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, comment_pk):
        return get_object_or_404(Comment, pk=comment_pk)

    def put(self, request, comment_pk):
        comment = self.get_object(comment_pk)
        serializer = CommentSerializer(
            comment, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, comment_pk):
        comment = self.get_object(comment_pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@ api_view(["GET"])
def check_sql(request):
    from django.db import connection

    # 정참조
    # comments = Comment.objects.all().select_related("article")
    # for comment in comments:
    #     print(comment.article.title)

    # 정참조에서 prefetch_related 사용가능

    # 역참조
    articles = Article.objects.all().prefetch_related("comments")
    for article in articles:
        comments = article.comments.all()
        for comment in comments:
            print(comment.content)

    print("-" * 30)
    print(connection.queries)

    return Response()
