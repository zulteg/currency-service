import requests
import json

from furl import furl
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from .exceptions import ServiceUnavailable
from .serializers import FilterSerializer, RateSerializer

STATS_URL = 'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange'


class IndexView(APIView):
    @swagger_auto_schema(
        operation_description="Get today's exchange rates",
        responses={
            200: RateSerializer(many=True),
            503: ServiceUnavailable.default_detail
        }
    )
    def get(self, request):
        url = furl(STATS_URL).add({'json': 1})

        try:
            response = requests.get(url)
            response_json = json.loads(response.content)
        except Exception:
            raise ServiceUnavailable

        rates = RateSerializer(data=response_json, many=True)
        rates.is_valid()

        return Response(rates.data)


class FilterView(APIView):
    @swagger_auto_schema(
        operation_description="Get exchange rates by currency and date range",
        query_serializer=FilterSerializer,
        responses={
            200: RateSerializer(many=True),
            400: "Bad Request",
            503: ServiceUnavailable.default_detail
        }
    )
    def get(self, request):
        params = FilterSerializer(data=request.query_params)
        params.is_valid(raise_exception=True)

        data = []
        for date in params.get_date_range():
            url = furl(STATS_URL).add({
                'valcode': params.data.get('code'),
                'date': date,
                'json': 1
            })

            try:
                response = requests.get(url)
                response_json = json.loads(response.content)
            except Exception:
                raise ServiceUnavailable

            rates = RateSerializer(data=response_json, many=True)
            rates.is_valid()

            data.extend(rates.data)

        return Response(data)
