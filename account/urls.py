from django.urls import path
from account.views import (
    MyObtainTokenPairView, RegisterView,ChangePasswordView,
    ResetPasswordView,ExampleView, MobileRegisterView,MobileLoginView,
    MobileLogoutView,ProfileView
)
from rest_framework_simplejwt.views import TokenRefreshView,TokenVerifyView

from rest_framework.views import exception_handler
from http import HTTPStatus
def api_exception_handler(exc, context):
    """Custom API exception handler."""

    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if response is not None:
        # Using the description's of the HTTPStatus class as error message.
        http_code_to_message = {v.value: v.description for v in HTTPStatus}

        error_payload = {
            "error": {
                "status_code": 0,
                "message": "",
                "details": [],
            }
        }
        error = error_payload["error"]
        status_code = response.status_code

        error["status_code"] = status_code
        error["message"] = http_code_to_message[status_code]
        error["details"] = response.data
        response.data = error_payload
    return response


urlpatterns = [
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    #path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('mobile_register/', MobileRegisterView.as_view(), name='auth_register'),
    path('mobile_login/', MobileLoginView.as_view(), name='mobile_login'),
    path('mobile_logout/', MobileLogoutView.as_view(), name='mobile_logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('test/', ExampleView.as_view(), name='ExampleView'),
]