import unittest
from unittest.mock import patch
from urllib.parse import urlencode, parse_qsl

import pytest
from fastapi import HTTPException

from models.pydantic.auth import TelegramUserInitData, \
    TelegramInitData  # Ensure this import is correct based on your project structure
from services.telegram import TelegramInitDataService  # Replace 'your_module' with the actual module name


class TestTelegramInitDataService(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.bot_token = "your_bot_token"
        self.service = TelegramInitDataService(self.bot_token)

    async def test_check_webapp_signature_valid(self):
        tg_user = {
            "id": "123456",
            "username": 'johndoe',
            "first_name": "John",
            'last_name': 'Doe',
            'language_code': 'en',
            'allows_write_to_pm': True,
            'photo_url': 'http://example.com/photo.jpg',
        }

        init_data_dict = {
            "user": tg_user,
            "chat_instance": "987654321",
            "auth_date": "1633036800",  # Example timestamp
        }
        init_data = TelegramInitData(
            **init_data_dict
        )

        # Generate the signature for the test data
        query_string = await self.service.generate_webapp_signature_data(init_data)

        # Check the signature
        is_valid = self.service.check_webapp_signature(query_string)
        self.assertTrue(is_valid)



    async def test_check_webapp_signature_invalid(self):
        # Simulate invalid data by tampering with the hash
        tg_user = {
            "id": "123456",
            "username": 'johndoe',
            "first_name": "John",
            'last_name': 'Doe',
            'language_code': 'en',
            'allows_write_to_pm': True,
            'photo_url': 'http://example.com/photo.jpg',
        }

        init_data_dict = {
            "user": tg_user,
            "chat_instance": "987654321",
            "auth_date": "1633036800",  # Example timestamp
        }
        init_data = TelegramInitData(
            **init_data_dict
        )

        # Generate a valid query string
        valid_query_string = await self.service.generate_webapp_signature_data(init_data)

        # Tamper with the hash to make it invalid
        invalid_query_string = valid_query_string.replace('hash=', 'hash=invalidhash')

        is_valid = await self.service.check_webapp_signature(invalid_query_string)
        self.assertFalse(is_valid)

    async def test_validated_telegram_init_data_success(self):
        tg_user = {
            "id": "123456",
            "username": 'johndoe',
            "first_name": "John",
            'last_name': 'Doe',
            'language_code': 'en',
            'allows_write_to_pm': True,
            'photo_url': 'http://example.com/photo.jpg',
        }

        init_data_dict = {
            "user": tg_user,
            "chat_instance": "987654321",
            "auth_date": "1633036800",  # Example timestamp
        }
        init_data = TelegramInitData(
            **init_data_dict
        )
        query_string = await self.service.generate_webapp_signature_data(init_data)
        result = await self.service.validated_telegram_init_data(query_string)
        self.assertIsInstance(result, TelegramInitData)
        self.assertEqual(result.user.id, 123456)
        self.assertEqual(result.user.first_name, 'John')

    async def test_validated_telegram_init_data_invalid(self):
        # Invalid data (missing hash)
        invalid_data = {
            'id': 123456,
            'first_name': 'John'
        }

        query_string = urlencode(invalid_data)

        with pytest.raises(HTTPException):
            await self.service.validated_telegram_init_data(query_string)

