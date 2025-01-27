import requests
import base58
import json
import time
from datetime import datetime, timedelta
from nacl.signing import SigningKey
from nacl.encoding import RawEncoder
from termcolor import colored

# Path file
ACCOUNTS_PATH = './accounts.txt'
PROXY_PATH = './proxies.txt'

# Log function to track activity
def log(pub_key, message, log_type='info'):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    colors = {
        'success': 'green',
        'error': 'red',
        'warning': 'yellow',
        'system': 'cyan',
        'info': 'magenta'
    }
    color = colors.get(log_type, 'white')
    if pub_key:
        print(colored(f"[{now}] [{pub_key}] {message}", color))
    else:
        print(colored(f"[{now}] {message}", color))

# Read accounts from file
def read_accounts():
    try:
        with open(ACCOUNTS_PATH, 'r') as f:
            accounts = [
                dict(zip(['token', 'refresh_token', 'private_key'], line.strip().split(':')))
                for line in f if line.strip()
            ]
        return accounts
    except Exception as e:
        log(None, f"Failed to read accounts: {e}", 'error')
        return []

# Read proxies from file (optional)
def read_proxies():
    try:
        with open(PROXY_PATH, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except:
        return []

# Update account file
def update_account_file(accounts):
    with open(ACCOUNTS_PATH, 'w') as f:
        f.write('\n'.join(f"{acc['token']}:{acc['refresh_token']}:{acc['private_key']}" for acc in accounts))

# Get public key from private key
def get_public_key(private_key):
    try:
        decoded_key = base58.b58decode(private_key.strip())
        signing_key = SigningKey(decoded_key)
        return signing_key.verify_key.encode().hex()
    except Exception as e:
        log(None, f"Failed to get public key: {e}", 'error')
        return 'UNKNOWN'

# Custom fetch function with optional proxy
def custom_fetch(url, method='GET', headers=None, data=None, proxy=None):
    proxies = {'http': proxy, 'https': proxy} if proxy else None
    try:
        response = requests.request(
            method,
            url,
            headers=headers,
            json=data,
            proxies=proxies,
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        log(None, f"Request failed: {e}", 'error')
        return {}

# Get login message
def get_login_message(fetch_func):
    return fetch_func('https://api.assisterr.ai/incentive/auth/login/get_message/')

# Sign login message
def sign_login_message(message, private_key):
    signing_key = SigningKey(base58.b58decode(private_key.strip()), encoder=RawEncoder)
    signed_message = signing_key.sign(message.encode())
    return {
        'signature': base58.b58encode(signed_message.signature).decode(),
        'public_key': signing_key.verify_key.encode().hex()
    }

# Handle login
def handle_login(fetch_func, message, private_key):
    signature_data = sign_login_message(message, private_key)
    payload = {
        'message': message,
        'signature': signature_data['signature'],
        'key': signature_data['public_key']
    }
    return fetch_func('https://api.assisterr.ai/incentive/auth/login/', method='POST', data=payload)

# Refresh token
def handle_token_refresh(fetch_func, refresh_token):
    headers = {'authorization': f"Bearer {refresh_token}"}
    return fetch_func('https://api.assisterr.ai/incentive/auth/refresh_token/', method='POST', headers=headers)

# Claim daily reward
def claim_daily(fetch_func, token):
    headers = {'authorization': f"Bearer {token}"}
    return fetch_func('https://api.assisterr.ai/incentive/users/me/daily_points/', method='POST', headers=headers)

# Check user status
def check_user_status(fetch_func, token):
    headers = {'authorization': f"Bearer {token}"}
    return fetch_func('https://api.assisterr.ai/incentive/users/me/', headers=headers)

# Process single account
def process_account(account, proxy=None):
    fetch_func = lambda url, **kwargs: custom_fetch(url, proxy=proxy, **kwargs)
    public_key = get_public_key(account['private_key'])

    try:
        log(public_key, "Processing account...", 'info')
        user_status = check_user_status(fetch_func, account['token'])

        if not user_status.get('id'):
            log(public_key, "Token expired, attempting refresh...", 'warning')
            refresh_result = handle_token_refresh(fetch_func, account['refresh_token'])
            if 'access_token' in refresh_result:
                account['token'] = refresh_result['access_token']
                account['refresh_token'] = refresh_result['refresh_token']
                log(public_key, "Token refreshed successfully", 'success')
            else:
                log(public_key, "Token refresh failed, attempting re-login...", 'error')
                login_message = get_login_message(fetch_func)
                login_result = handle_login(fetch_func, login_message, account['private_key'])
                if 'access_token' in login_result:
                    account['token'] = login_result['access_token']
                    account['refresh_token'] = login_result['refresh_token']
                    log(public_key, "Login successful", 'success')
                else:
                    raise Exception("Login failed")

        claim_result = claim_daily(fetch_func, account['token'])
        if 'points' in claim_result:
            log(public_key, f"Successfully claimed {claim_result['points']} points", 'success')
        else:
            log(public_key, f"Claim failed: {claim_result}", 'error')

    except Exception as e:
        log(public_key, f"Error: {e}", 'error')

    return account

# Main function
def main():
    log(None, "Daily automation script started!", 'system')
    accounts = read_accounts()
    proxies = read_proxies()

    if proxies:
        log(None, f"{len(proxies)} proxies found", 'info')
    else:
        log(None, "No proxies found, using direct connection", 'warning')

    updated_accounts = []
    for i, account in enumerate(accounts):
        proxy = proxies[i % len(proxies)] if proxies else None
        updated_accounts.append(process_account(account, proxy))

    update_account_file(updated_accounts)
    log(None, "All accounts processed, waiting for the next cycle...", 'system')
    time.sleep(3600)
    main()

# Run script
if __name__ == "__main__":
    main()