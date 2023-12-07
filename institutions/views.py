from rest_framework import viewsets
from .models import Institution
from .serializers import InstitutionSerializer,InstitutionCreationSerializer
from djoser.permissions import CurrentUserOrAdminOrReadOnly

# Create your views here.
class InstituteViewSet(viewsets.ModelViewSet):
    queryset = Institution.objects.all()
    permission_classes = [CurrentUserOrAdminOrReadOnly]
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
