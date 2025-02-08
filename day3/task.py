import requests
import json

# Define the API URL
API_URL = "https://api.sunrise-sunset.org/json?lat=36.7201600&lng=-4.4203400"

def task(api_url=API_URL):
    try:
        response = requests.get(api_url, timeout=10)  # Set timeout for reliability

        if response.status_code == 200:
            data = response.json()  # Convert response to JSON
            print(" API response received successfully.")

            # Save to a JSON file
            file_path = "api1_response.json"
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)

            print(f"API response saved to '{file_path}'.")
            return data  #  Returns API response for further use
        
        else:
            print(f" Failed to retrieve data. Status code: {response.status_code}")
            return None

    except requests.Timeout:
        print(" Error: The request timed out.")
        return None

    except requests.RequestException as e:
        print(f" Error making API request: {e}")
        return None
