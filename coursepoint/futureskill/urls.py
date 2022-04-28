from django.contrib import admin
from django.urls import path, include
from . import views

from django.conf.urls.static import static
from django.conf import settings
from .views import UserViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)


urlpatterns = [
    path('', views.index, name="home"),
    path('registration', views.signup, name="signup"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('checkout/<str:slug>', views.checkout, name="checkout"),
    path('course/<str:slug>', views.course_informations, name="cour"),
    path('verify_payment', views.verify_payment, name="verify_payment"),
    path('mycourse', views.mycourse, name='my_course'),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))




]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
