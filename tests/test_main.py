import pytest
from unittest.mock import patch
from main import CurrencyService

@patch('main.requests.get')

def test_get_rates_success(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "base": "USD",
        "rates": {"USD": 1.0, "EUR": 0.85}
    }
    
    rates = CurrencyService.get_rates("USD")
    assert rates["EUR"] == 0.85
    assert rates["USD"] == 1.0

@patch('main.requests.get')
def test_get_rates_failure(mock_get):
    import requests
    mock_get.side_effect = requests.RequestException("Network Error")
    
    with pytest.raises(ConnectionError):
        CurrencyService.get_rates("USD")
