from django.shortcuts import render
from rest_framework import viewsets,permissions
from .models import Institution, Application
from .serializers import InstitutionSerializer,InstitutionCreationSerializer,ApplicationSerializer,ApplicationCreationSerializer

# Create your views here.
class InstituteViewSet(viewsets.ModelViewSet):
    queryset = Institution.objects.all()
    permission_classes = [permissions.AllowAny]
    lookup_field = 'abbreviation'


    def get_serializer_class(self):
        if self.action == 'list':
            return InstitutionSerializer
        elif self.action == 'retrieve':
            return InstitutionSerializer
        elif self.action == 'create':
            return InstitutionCreationSerializer
        elif self.action == 'update':
            return InstitutionCreationSerializer
        elif self.action == 'partial_update':
            return InstitutionCreationSerializer
        elif self.action == 'destroy':
            return InstitutionCreationSerializer
        else:
            return InstitutionSerializer
