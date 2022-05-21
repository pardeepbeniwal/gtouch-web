from django.urls import path
from account.views import (
    MyObtainTokenPairView, RegisterView,ChangePasswordView,
    ForgotPasswordView,ResetPasswordView,ExampleView
)
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    #path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    
    path('test/', ExampleView.as_view(), name='ExampleView'),
]