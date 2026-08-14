import os
from unittest.mock import AsyncMock, MagicMock, patch
import httpx

os.environ.setdefault('WEATHER_API_KEY', 'test-key')

from mcp_server import get_weather


async def test_get_weather_success():
    fake_response = MagicMock()
    fake_response.status_code = 200
    fake_response.json.return_value = {
        'name': 'New York',
        'sys': {'country': 'US'},
        'main': {'temp': 15.0, 'humidity': 80},
        'wind': {'speed': 10.0}
    }
    fake_response.raise_for_status.return_value = None

    with patch.object(httpx.AsyncClient, 'get', AsyncMock(return_value=fake_response)):
        result = await get_weather('New York')

    assert 'New York' in result
    assert 'US' in result
    assert '15.0' in result


async def test_get_weather_unknown_city():
    fake_response = MagicMock()
    fake_response.status_code = 400

    with patch.object(httpx.AsyncClient, 'get', AsyncMock(return_value=fake_response)):
        result = await get_weather('Fake City')

    assert 'Fake City' in result


async def test_get_weather_network_error():
    with patch.object(httpx.AsyncClient, 'get', AsyncMock(side_effect=httpx.RequestError('Network Error'))):
        result = await get_weather('Paris')

    assert result == 'Could not reach the weather service to check Paris'
