import requests
import json
import sys
from requests.exceptions import RequestException

def test_login():
    try:
        # Test login endpoint
        login_url = 'http://localhost:6543/auth/login'
        login_data = {
            'email': 'user@example.com',
            'password': 'Password123'
        }
        
        print('Attempting login...')
        response = requests.post(login_url, json=login_data, timeout=5)
        
        print('\nLogin Response:')
        print(f'Status code: {response.status_code}')
        print('Headers:')
        for key, value in response.headers.items():
            print(f'  {key}: {value}')
        print('\nBody:')
        try:
            print(json.dumps(response.json(), indent=2))
        except ValueError:
            print(response.text)
        
        if response.ok:
            data = response.json()
            token = data.get('token')
            if token:
                print('\nTesting /bookings endpoint with token...')
                bookings_url = 'http://localhost:6543/bookings'
                headers = {
                    'Authorization': f'Bearer {token}',
                    'Content-Type': 'application/json'
                }
                print('\nRequest Headers:')
                print(json.dumps(headers, indent=2))
                
                bookings_response = requests.get(bookings_url, headers=headers, timeout=5)
                print('\nBookings Response:')
                print(f'Status code: {bookings_response.status_code}')
                print('Headers:')
                for key, value in bookings_response.headers.items():
                    print(f'  {key}: {value}')
                print('\nBody:')
                try:
                    print(json.dumps(bookings_response.json(), indent=2))
                except ValueError:
                    print(bookings_response.text)
            else:
                print('\nNo token found in response')
    except RequestException as e:
        print(f'\nError: {e}')
        print('Make sure the server is running and accessible')
        sys.exit(1)

if __name__ == '__main__':
    test_login() 