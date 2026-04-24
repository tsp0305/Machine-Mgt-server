import urllib.request
import json
import urllib.error

BASE_URL = "http://localhost:8080/api/auth"

def make_request(url, data=None):
    if data:
        data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'}, method='POST')
    try:
        with urllib.request.urlopen(req) as response:
            return response.status, json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode('utf-8'))

def test():
    print("Testing Signup Happy Path...")
    status, data = make_request(f"{BASE_URL}/signup", {
        "email": "test_unique_2@example.com",
        "password": "StrongPass123"
    })
    print("Status:", status, data)

    print("Testing Signup Duplicate...")
    status, data = make_request(f"{BASE_URL}/signup", {
        "email": "test_unique_2@example.com",
        "password": "StrongPass123"
    })
    print("Status:", status, data)

    print("Testing Signup Weak Password...")
    status, data = make_request(f"{BASE_URL}/signup", {
        "email": "newuser@example.com",
        "password": "short"
    })
    print("Status:", status, type(data))

    print("Testing Login Wrong Password...")
    status, data = make_request(f"{BASE_URL}/login", {
        "email": "test_unique_2@example.com",
        "password": "WrongPassword!"
    })
    print("Status:", status, data)

if __name__ == "__main__":
    test()
