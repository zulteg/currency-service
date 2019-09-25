import datetime

from rest_framework import serializers

FILTER_DATE_FORMAT = '%Y%m%d'
MAX_DATE_RANGE = 31
AVAILABLE_CODE = ['AUD', 'CAD', 'CNY', 'HRK', 'CZK', 'DKK', 'HKD', 'HUF',
                  'INR', 'IDR', 'IRR', 'ILS', 'JPY', 'KZT', 'KRW', 'MXN',
                  'MDL', 'NZD', 'NOK', 'RUB', 'SAR', 'SGD', 'ZAR', 'SEK',
                  'CHF', 'EGP', 'GBP', 'USD', 'BYN', 'AZN', 'RON', 'TRY',
                  'XDR', 'BGN', 'EUR', 'PLN', 'DZD', 'BDT', 'AMD', 'IQD',
                  'KGS', 'LBP', 'LYD', 'MYR', 'MAD', 'PKR', 'VND', 'THB',
                  'AED', 'TND', 'UZS', 'TWD', 'TMT', 'GHS', 'RSD', 'TJS',
                  'GEL', 'XAU', 'XAG', 'XPT', 'XPD']


class RateSerializer(serializers.Serializer):
    r030 = serializers.IntegerField(label='Digital currency code')
    txt = serializers.CharField(label='Currency name')
    rate = serializers.FloatField(label='Rate')
    cc = serializers.CharField(label='Currency code')
    exchangedate = serializers.DateField(label='Exchange date')


class FilterSerializer(serializers.Serializer):
    code = serializers.CharField(
        min_length=3,
        max_length=3,
        help_text='ISO currency code (USD, EUR, ...)'
    )
    from_date = serializers.DateField(
        format=FILTER_DATE_FORMAT,
        input_formats=[FILTER_DATE_FORMAT],
        help_text='In format YYYYMMDD'
    )
    to_date = serializers.DateField(
        format=FILTER_DATE_FORMAT,
        input_formats=[FILTER_DATE_FORMAT],
        help_text='In format YYYYMMDD'
    )

    def validate_code(self, value):
        if value.upper() not in AVAILABLE_CODE:
            raise serializers.ValidationError("Invalid code field value.")
        return value

    def validate_from_date(self, value):
        if value > datetime.date.today():
            raise serializers.ValidationError(
                "from_date must be less or equal to today date.")
        return value

    def validate_to_date(self, value):
        if value > datetime.date.today():
            raise serializers.ValidationError(
                "to_date must be less or equal to today date.")
        return value

    def validate(self, attrs):
        delta = (attrs.get('to_date') - attrs.get('from_date')).days
        if delta > MAX_DATE_RANGE:
            raise serializers.ValidationError({
                'date': f"Date range is too big. Max range: {MAX_DATE_RANGE} days."
            })
        if attrs.get('from_date') > attrs.get('to_date'):
            raise serializers.ValidationError({
                'date': "from_date field must be equal or less than to_date field."
            })
        return attrs

    def get_date_range(self):
        from_date = datetime.datetime.strptime(
            self.data.get('from_date'),
            FILTER_DATE_FORMAT
        )
        to_date = datetime.datetime.strptime(
            self.data.get('to_date'),
            FILTER_DATE_FORMAT
        )

        date_range = []
        for days in range(0, (to_date - from_date).days + 1):
            date = from_date + datetime.timedelta(days=days)
            date_range.append(date.strftime(FILTER_DATE_FORMAT))

        return date_range
