from drf_yasg.utils import swagger_auto_schema
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken

from .serializers import TokenSerializer


class CustomObtainAuthToken(ObtainAuthToken):
    @swagger_auto_schema(
        operation_description="Generate user auth token",
        request_body=AuthTokenSerializer,
        responses={
            200: TokenSerializer,
            400: "Bad Request",
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
