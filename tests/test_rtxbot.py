from unittest.mock import AsyncMock
import asyncio
import pytest
import requests
import requests_mock
from bot.rtxbot import RTXBot

@pytest.fixture
def bot():
    """
    Pytest fixture to create an instance of the RTXBot class.

    Returns:
        RTXBot: An instance of the RTXBot class with a mock channel and a fictitious URL.
    """
    token = "your_token"
    url = "https://example.com/api" # Fictitious URL for testing
    rtxbot = RTXBot(token, None, url)
    rtxbot.channel = AsyncMock()
    return rtxbot

@pytest.fixture
def mock_request():
    """
    Pytest fixture to mock HTTP requests using requests_mock.

    Yields:
        Mocker: A requests_mock.Mocker instance for mocking HTTP requests.
    """
    with requests_mock.Mocker() as mock:
        yield mock

def test_check_stock_success(bot, mock_request):
    """
    Test to ensure successful stock check retrieves correct product information.

    Args:
        bot (RTXBot): The RTXBot instance to be tested.
        mock_request (Mocker): The mock object for HTTP requests.
    """
    # Mock a successful JSON response
    mock_request.get(bot.url, json={
        "searchedProducts": {
            "featuredProduct": {
                "productAvailable": True,
                "productTitle": "NVIDIA RTX 4090",
                "productPrice": "1499.99",
                "retailers": [{"purchaseLink": "http://example.com/purchase"}]
            }
        }
    })

    response = asyncio.run(bot.check_stock())
    assert response.get('productAvailable') is True
    assert response.get('productTitle') == "NVIDIA RTX 4090"
    assert response.get('productPrice') == "1499.99"
    assert response.get('retailers')[0].get('purchaseLink') == "http://example.com/purchase"

def test_check_stock_failure(bot, mock_request):
    """
    Test to check handling of failed stock check (e.g., HTTP 500 response).

    Args:
        bot (RTXBot): The RTXBot instance to be tested.
        mock_request (Mocker): The mock object for HTTP requests.
    """
    # Mock a failure response
    mock_request.get(bot.url, status_code=500)

    response = asyncio.run(bot.check_stock())
    assert response == "Failed to retrieve information from NVIDIA API."

def test_check_stock_exception(bot, mock_request):
    """
    Test to check handling of exceptions during stock check (e.g., network issues).

    Args:
        bot (RTXBot): The RTXBot instance to be tested.
        mock_request (Mocker): The mock object for HTTP requests.
    """
    # Mock a request exception
    mock_request.get(bot.url, exc=requests.exceptions.RequestException)

    response = asyncio.run(bot.check_stock())
    assert "Error during NVIDIA API request" in response

async def run_periodic_task(task, interval_seconds):
    """
    Helper function to manually run a periodic task for testing.

    Args:
        task (coroutine): The asynchronous task to be run.
        interval_seconds (int): The interval in seconds between task runs.
    """
    for _ in range(2):
        await task()
        await asyncio.sleep(interval_seconds)

def test_check_stock_periodically(bot, mock_request):
    """
    Test to ensure periodic stock check updates the stock status correctly.

    Args:
        bot (RTXBot): The RTXBot instance to be tested.
        mock_request (Mocker): The mock object for HTTP requests.
    """
    # Mock responses for two stock checks with different availability
    mock_request.get(bot.url, [
        {'json': {
            "searchedProducts": {
                "featuredProduct": {
                    "productAvailable": False,  # Première vérification: non disponible
                    "productTitle": "NVIDIA RTX 4090",
                    "productPrice": "1499.99",
                    "retailers": [{"purchaseLink": "http://example.com/purchase"}]
                }
            }
        }},
        {'json': {
            "searchedProducts": {
                "featuredProduct": {
                    "productAvailable": True,  # Deuxième vérification: disponible
                    "productTitle": "NVIDIA RTX 4090",
                    "productPrice": "1499.99",
                    "retailers": [{"purchaseLink": "http://example.com/purchase"}]
                }
            }
        }}
    ])

    asyncio.run(run_periodic_task(bot.check_stock_periodically, 2))
    bot.channel.send.assert_called()
    assert bot.last_status == "Available"
