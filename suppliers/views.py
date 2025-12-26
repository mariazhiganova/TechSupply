from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from suppliers.models import Supplier
from suppliers.serializers import SupplierSerializer
from users.permissions import IsActiveUser


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsActiveUser]
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ['country']
