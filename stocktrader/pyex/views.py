from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status


class PyexViewSet(viewsets.GenericViewSet):
    @action(detail=False, methods=['get'])
    def get_company_data(self, request):
        pass

    @action(detail=False, methods=['get'])
    def get_companies(self, request):
        pass
