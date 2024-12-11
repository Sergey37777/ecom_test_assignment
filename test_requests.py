import requests

BASE_URL = "http://localhost:8000"

def test_form_matching():
    print("Testing form matching...")
    data = {
        "fields": {
            "f_name1": "example@example.com",
            "f_name2": "+7 123 456 78 90"
        }
    }
    response = requests.post(f"{BASE_URL}/get_form", json=data)
    print("Request data:", data)
    print("Response:", response.json())

def test_form_typing():
    print("Testing form field typing...")
    data = {
        "fields": {
            "f_name1": "wrong_email_format",
            "f_name2": "2024-12-11"
        }
    }
    response = requests.post(f"{BASE_URL}/get_form", json=data)
    print("Request data:", data)
    print("Response:", response.json())

def run_tests():
    print("Starting tests...")
    test_form_matching()
    print()
    test_form_typing()
    print("Tests completed.")

if __name__ == "__main__":
    run_tests()
