import hashlib
import hmac
from operator import itemgetter
from typing import Dict
from urllib.parse import parse_qsl, urlencode, quote_plus

from models.pydantic.auth import TelegramInitData


class TelegramInitDataService:
    def __init__(self, bot_token: str):
        self.token = bot_token

    async def validated_telegram_init_data(self, init_data: str) -> TelegramInitData | None:
        data_verified = await self.check_webapp_signature(init_data=init_data)
        if not data_verified:
            return None
        parsed_data = dict(parse_qsl(init_data))
        init_data = TelegramInitData(**parsed_data)
        return init_data

    async def check_webapp_signature(self, init_data: str) -> bool:
        """
        Check incoming WebApp init data signature

        Source: https://core.telegram.org/bots/webapps#validating-data-received-via-the-web-app
        """
        try:
            parsed_data = dict(parse_qsl(init_data))
        except ValueError:
            # Init data is not a valid query string
            return False
        if "hash" not in parsed_data:
            # Hash is not present in init data
            return False

        hash_ = parsed_data.pop('hash')
        data_check_string = "\n".join(
            f"{k}={v}" for k, v in sorted(parsed_data.items(), key=itemgetter(0))
        )
        secret_key = hmac.new(
            key=b"WebAppData", msg=self.token.encode(), digestmod=hashlib.sha256
        )
        calculated_hash = hmac.new(
            key=secret_key.digest(), msg=data_check_string.encode(), digestmod=hashlib.sha256
        ).hexdigest()
        return calculated_hash == hash_

    async def generate_webapp_signature_data(self, data: Dict[str, str]) -> str:
        """
        Generate a query string that will pass the web app signature check.

        Args:
            data (Dict[str, str]): The data to include in the query string.

        Returns:
            str: A query string with a valid signature hash.
        """
        # Sort the data and create the data check string
        sorted_items = sorted(data.items())
        data_check_string = "\n".join(f"{k}={v}" for k, v in sorted_items)

        # Create the secret key
        secret_key = hmac.new(
            key=b"WebAppData", msg=self.token.encode(), digestmod=hashlib.sha256
        )

        # Calculate the hash
        calculated_hash = hmac.new(
            key=secret_key.digest(), msg=data_check_string.encode(), digestmod=hashlib.sha256
        ).hexdigest()

        # Add the hash to the data
        data['hash'] = calculated_hash

        # Create the final query string
        query_string = urlencode(data, quote_via=quote_plus)
        return query_string