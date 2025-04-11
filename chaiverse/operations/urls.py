from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from .views import *
urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', OwnerDetails.as_view(), name="register"),
    path('login/', LoginAPIView.as_view(), name= "login"),
    path('users/', OwnerDetails.as_view(), name='users'),
    path('users/<int:user_id>/shops/',ShopAPIView.as_view(), name="shops"),
    path('users/<int:user_id>/shop/<int:shop_id>/products/', ProductAPIView.as_view(), name="products"),
 
]