# -*- coding: BIG5 -*-
#views.py
import datetime
from .models import ForSystem, TrcTech
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User, Group
from .serializers import TrcTechSerializer, UserSerializer, GroupSerializer, TokenSerializer
from django.contrib.auth import password_validation
from django.contrib.auth.hashers import make_password
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.pagination import PageNumberPagination
from .permissions import IsPosterOrReadOnly, IsManagers, IsUser
from .collector import *


class NewsCrawlerAPI(viewsets.GenericViewSet):
    serializer_class = TrcTechSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsManagers]
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not self.check_title(request.data.get("news_title")):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"error": "News is already exist!"}, status=status.HTTP_208_ALREADY_REPORTED)

    def check_title(self, title):
        return TrcTech.objects.filter(news_title=title).exists()


class GetNewsListAPI(viewsets.ModelViewSet):
    pagination_class = PageNumberPagination
    serializer_class = TrcTechSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        source = self.request.query_params.get("source", "all")
        if source == "all":
            queryset = TrcTech.objects.all().order_by("-news_date")
        elif source =="udn":
            queryset = TrcTech.objects.filter(news_source="聯合新聞網").order_by("-news_date")
        elif source =="apple":
            queryset = TrcTech.objects.filter(news_source="壹蘋新聞網").order_by("-news_date")
        else:
            queryset = TrcTech.objects.all().order_by("-news_date")
        return queryset

    def list(self, request, *args, **kwargs):
        sys_item = ForSystem.objects.get(id="1")
        check_time = datetime.datetime.strptime(sys_item.check_time, "%Y-%m-%d %H:%M")

        if datetime.datetime.now() > (check_time + datetime.timedelta(minutes=30)):
            collect_news(sys_item.check_time)
            sys_item.check_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
            sys_item.save()
        
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        return Response({"message": "unauthorized!!!"}, status=status.HTTP_401_UNAUTHORIZED)

    def retrieve(self, request, *args, **kwargs):
        return Response({"message": "unauthorized!!!"}, status=status.HTTP_401_UNAUTHORIZED)

    def update(self, request, *args, **kwargs):
        return Response({"message": "unauthorized!!!"}, status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, *args, **kwargs):
        return Response({"message": "unauthorized!!!"}, status=status.HTTP_401_UNAUTHORIZED)


class RegisterAPI(viewsets.GenericViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        User.objects.create_user(serializer.validated_data["username"], serializer.validated_data["email"], serializer.validated_data["password"])
        return Response(serializer.data, status= status.HTTP_201_CREATED)


class LoginAPI(viewsets.GenericViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


    def create(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({"message": "Login Successful!", "token": token.key}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid Credentials!"}, status=status.HTTP_401_UNAUTHORIZED)


class Logout(viewsets.GenericViewSet):
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        logout(request)
        return Response({"message": "Logout Successful!"}, status=status.HTTP_200_OK)


class UserDataEdit(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsUser]
    lookup_field = 'pk'


    def create(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def list(self, request, *args, **kwargs):
        try:
            user = User.objects.get(username=request.user.username)
        except Exception as e:
            return Response({"error": e}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data["password"] = make_password(request.data["password"])
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
