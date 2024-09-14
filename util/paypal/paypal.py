import requests
from requests.auth import HTTPBasicAuth
import os

PAYPAL_CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID")
PAYPAL_SECRET = os.getenv("PAYPAL_CLIENT_SECRET")
# Use 'https://api-m.paypal.com' for live environment
PAYPAL_API_BASE_URL = os.getenv("PAYPAL_API_BASE_URL")


def get_paypal_access_token():
    url = f'{PAYPAL_API_BASE_URL}/v1/oauth2/token'
    response = requests.post(
        url,
        headers={'Accept': 'application/json', 'Accept-Language': 'en_US'},
        data={'grant_type': 'client_credentials'},
        auth=HTTPBasicAuth(PAYPAL_CLIENT_ID, PAYPAL_SECRET)
    )
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        raise Exception(f"Failed to get PayPal access token: {response.text}")
    
def get_token_info(access_token, client_id, client_secret):

    # PayPal sandbox URL for token introspection
    url = f"{PAYPAL_API_BASE_URL}/v1/oauth2/token/introspect"

    # Headers
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # Data (token to introspect)
    data = {
        "token": access_token
    }

    # Make a POST request to introspect the token
    response = requests.post(url, headers=headers, data=data,
                            auth=HTTPBasicAuth(client_id, client_secret))
    print(response)

    if response.status_code == 200:
        token_info = response.json()
        print("Token info:", token_info)
    else:
        print(f"Failed to introspect token. Status code: {response.status_code}")
        print("Response:", response.text)


def get_user_info(access_token):
    url = f'{PAYPAL_API_BASE_URL}/v1/identity/oauth2/userinfo?schema=paypalv1.1'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to get user info: {response.text}")


def create_product(access_token):

    url = f"{PAYPAL_API_BASE_URL}/v1/catalogs/products"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    data = {
        "name": "Netflix test",
        "description": "A sample product for testing.",
        "type": "SERVICE",  # or "PHYSICAL" for physical products
        "category": "SOFTWARE",
        "image_url": "https://example.com/product-image.jpg",
        "home_url": "https://example.com"
    }

    response = requests.post(url, headers=headers, json=data)
    print(response.text)

    if response.status_code == 201:
        product = response.json()
        print("Product created:", product)
        product_id = product["id"]
        print("Product ID:", product_id)
        return product_id

    else:
        print(f"Failed to create product. Status code: {response.status_code}")
        raise Exception(f"Failed to get PayPal subscriptions: {response.text}")


def create_plan(access_token, product_id):
    url = f"{PAYPAL_API_BASE_URL}/v1/billing/plans"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    data = {
        # Replace with a valid product ID or create a product first
        "product_id": product_id,
        "name": "Basic Plan",
        "description": "Monthly subscription plan",
        "billing_cycles": [
            {
                "frequency": {
                    "interval_unit": "MONTH",
                    "interval_count": 1
                },
                "tenure_type": "REGULAR",
                "sequence": 1,
                "total_cycles": 12,
                "pricing_scheme": {
                    "fixed_price": {
                        "value": "15.00",
                        "currency_code": "AUD"
                    }
                }
            }
        ],
        "payment_preferences": {
            "auto_bill_amount": "YES",
            "setup_fee": {
                "value": "0.00",
                "currency_code": "USD"
            },
            "payment_failure_threshold": 3
        },
        "taxes": {
            "percentage": "0",
            "inclusive": False
        }
    }

    response = requests.post(url, headers=headers, json=data)
    print(response.text)

    if response.status_code == 201:
        plan = response.json()
        print("Plan created:", plan)
        plan_id = plan["id"]
        print("Plan ID:", plan_id)
        return plan_id
    else:
        print(f"Failed to create plan. Status code: {response.status_code}")
        raise Exception(f"Failed to create plan: {response.text}")


def add_mock_plan(access_token, plan_id, user_email):

    url = f"{PAYPAL_API_BASE_URL}/v1/billing/subscriptions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    data = {
        "plan_id": plan_id,  # Use a mock plan ID if available
        "subscriber": {
            "name": {
                "given_name": "John",
                "surname": "Doe"
            },
            "email_address": user_email
        },
        "application_context": {
            "brand_name": "Your Business Name",
            "locale": "en-US",
            "shipping_preference": "NO_SHIPPING",
            "user_action": "SUBSCRIBE_NOW",
            "return_url": "https://github.com/",
            "cancel_url": "https://github.com/"
        }
    }

    response = requests.post(url, headers=headers, json=data)
    print(response.text)

    if response.status_code == 201:
        subscription = response.json()
        print("Subscription created:", subscription)
        approval_url = subscription["links"][0]["href"]
        print("User should approve subscription at:", approval_url)
        return approval_url
    else:
        print(
            f"Failed to create subscription. Status code: {response.status_code}")
        raise Exception(f"Failed to add mock plan: {response.text}")


def get_paypal_subscriptions(access_token):
    url = f'{PAYPAL_API_BASE_URL}/v1/billing/plans'
    response = requests.get(
        url,
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
    )
    print(response.status_code)
    print(response.text)
    if response.status_code == 200:
        return response.json()  # Parse and return the subscription data
    else:
        raise Exception(f"Failed to get PayPal subscriptions: {response.text}")
    

def get_access_code_from_uri_code(authorization_code, redirect_uri, client_id, client_secret):

    # PayPal sandbox URL for token exchange
    url = f"{PAYPAL_API_BASE_URL}/v1/oauth2/token"

    # Headers
    headers = {
        "Accept": "application/json",
        "Accept-Language": "en_US"
    }

    # Data for exchanging authorization code for access token
    data = {
        "grant_type": "authorization_code",
        "code": authorization_code,
        "redirect_uri": redirect_uri,
        "scope": "https://uri.paypal.com/services/subscription"
    }

    # Request access token using the authorization code
    response = requests.post(url, headers=headers, data=data,
                            auth=HTTPBasicAuth(client_id, client_secret))

    # Check if the request was successful
    if response.status_code == 200:
        token_data = response.json()
        print(token_data)
        access_token = token_data['access_token']
        print("Access token:", access_token)
        return access_token
    
    else:
        print(
            f"Failed to obtain access token. Status code: {response.status_code}")
        print("Response:", response.text)
        raise Exception(f"Failed to convert authentication code {response.text}")



if __name__ == "__main__":
    # Step 1: Get PayPal Access Token and Subscriptions
    access_token = get_paypal_access_token()
    print(access_token)
    # user_info = get_user_info(access_token=access_token)
    # print(user_info)
    subscriptions = get_paypal_subscriptions(access_token)
    print(subscriptions)
