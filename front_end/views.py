from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes
from rest_framework import authentication, permissions


@api_view(['GET'])
def about(request):
    return render(request, 'about.html')

@api_view(['GET'])
def login(request):
    return render(request, 'login.html')

@api_view(['GET'])
def logout(request):
    return Response()

class NexusElectricView(APIView):
    def get(self, request):
        return Response()
    
    def post(self, request):
        return Response()
