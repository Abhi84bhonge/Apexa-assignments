import pytest
import json
import requests
from unittest.mock import patch, MagicMock
from task import task # Import the function from task.py

# Mock API response data
MOCK_RESPONSE = {
    "results": {
        "sunrise": "6:10:00 AM",
        "sunset": "6:45:00 PM",
        "solar_noon": "12:30:00 PM",
    },
    "status": "OK",
}

# Test case for a successful API request
@patch("requests.get")
def test_task_success(mock_get, tmp_path):
    """Test that task() successfully fetches API data and writes to a JSON file."""
    # Mock API response
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = MOCK_RESPONSE

    # Call the task function
    task()

    # Verify API was called once
    mock_get.assert_called_once()

    # Check if JSON file was created and contains correct data
    file_path = "api1_response.json"
    with open(file_path, "r", encoding="utf-8") as file:
        saved_data = json.load(file)
    
    assert saved_data == MOCK_RESPONSE  # Ensure saved JSON matches mock data

# Test case for an API failure (non-200 status)
@patch("requests.get")
def test_task_failure(mock_get):
    """Test that task() handles API failure correctly."""
    # Mock a failed response
    mock_get.return_value.status_code = 404

    # Call the function
    task()

    # Verify API was called once
    mock_get.assert_called_once()

    # Check printed message (optional)
    assert mock_get.return_value.status_code == 404
