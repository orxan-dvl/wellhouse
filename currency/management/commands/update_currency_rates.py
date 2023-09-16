# your_app/management/commands/update_currency_rates.py

import requests
from django.core.management.base import BaseCommand
from currency.models import CurrencyModel  # Replace "your_app" with the actual name of your Django app
from requests.exceptions import RequestException



class Command(BaseCommand):
    help = 'Update currency rates in the database'


    def handle(self, *args, **kwargs):
        try:
            # Make a GET request to the API endpoint
            api_url = 'https://api.exchangerate.host/latest'
            response = requests.get(api_url)
            response.raise_for_status()  # Raise an exception for 4xx and 5xx errors

            data = response.json()
            rates = data.get('rates', {})

            # Update the database with the new currency rates
            currency_model, created = CurrencyModel.objects.get_or_create(pk=1)
            currency_model.try_rate = rates.get('TRY', 0)
            currency_model.rub_rate = rates.get('RUB', 0)
            currency_model.usd_rate = rates.get('USD', 0)
            currency_model.gbp_rate = rates.get('GBP', 0)
            currency_model.pln_rate = rates.get('PLN', 0)
            currency_model.nok_rate = rates.get('NOK', 0)
            currency_model.kzt_rate = rates.get('KZT', 0)
            currency_model.save()

        except RequestException as e:
            # Handle request-related exceptions (e.g., connection error)
            print(f"Request Exception: {e}")

        except ValueError as e:
            # Handle JSON decoding errors
            print(f"JSON Decode Error: {e}")
