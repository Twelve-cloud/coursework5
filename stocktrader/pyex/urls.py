from rest_framework.routers import DefaultRouter
from pyex import views


app_name = 'pyex'

router = DefaultRouter()

router.register(prefix='data', viewset=views.PyexViewSet, basename='pyex')

urlpatterns = router.urls
