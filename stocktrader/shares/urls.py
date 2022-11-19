from rest_framework.routers import DefaultRouter
from shares import views


router = DefaultRouter()

router.register(prefix='brokers', viewset=views.BrokerViewSet, basename='broker')
router.register(prefix='orders', viewset=views.OrderViewSet, basename='order')
router.register(prefix='accounts', viewset=views.AccountViewSet, basename='account')
router.register(prefix='stocks', viewset=views.AccountViewSet, basename='stock')
router.register(prefix='accounts-history', viewset=views.AccountViewSet, basename='account_history')

urlpatterns = router.urls
