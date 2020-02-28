from rest_framework import viewsets
from rest_framework.response import Response

class GetOnlyGenericViewset(viewsets.ViewSet):
    http_method_names = ['get']