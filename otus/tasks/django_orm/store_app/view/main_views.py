from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers


class AboutView(APIView):
    def get(self, request):
        """Страница о нас"""
        return JsonResponse(
            {
                "School": "OTUS",
                "Task": "Django ORM",
                "Year": "2026",
                "Student": "Vitaly Yunusov",
            }
        )

class IndexView(APIView):
    def get(self, request):
        """Страница index"""
        return JsonResponse({"response": "Store APP under construction"})

