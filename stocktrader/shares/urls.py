from rest_framework.routers import DefaultRouter
from shares import views


router = DefaultRouter()

router.register(prefix='brokers', viewset=views.BrokerViewSet, basename='broker')
router.register(prefix='orders', viewset=views.OrderViewSet, basename='order')
router.register(prefix='deals', viewset=views.DealViewSet, basename='deal')
router.register(prefix='accounts', viewset=views.AccountViewSet, basename='account')

urlpatterns = router.urls
