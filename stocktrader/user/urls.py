from rest_framework.routers import DefaultRouter
from user import views


router = DefaultRouter()

router.register(prefix='users', viewset=views.UserViewSet, basename='user')

urlpatterns = router.urls
