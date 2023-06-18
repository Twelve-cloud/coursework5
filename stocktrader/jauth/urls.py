from rest_framework.routers import DefaultRouter
from jauth import views


router = DefaultRouter()

router.register(prefix='jwt', viewset=views.AuthViewSet, basename='jwt')

urlpatterns = router.urls
