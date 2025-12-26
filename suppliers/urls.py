from rest_framework.routers import DefaultRouter

from suppliers.apps import SuppliersConfig
from suppliers.views import SupplierViewSet

app_name = SuppliersConfig.name

router = DefaultRouter()
router.register(r'', SupplierViewSet, basename='supplier')

urlpatterns = router.urls
