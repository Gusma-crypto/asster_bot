# asster_bot
automotion bot assister

# Daily Automation Script

This Python script automates daily tasks for account management, including logging in, refreshing tokens, and claiming daily rewards. It uses proxies to manage multiple accounts and logs activities for easier debugging and monitoring.

---

## Features

- **Account Handling**: Reads account details from a text file.
- **Proxy Support**: Supports proxy connections for requests.
- **Token Management**: Automatically refreshes tokens or re-logs if necessary.
- **Daily Rewards**: Claims daily points for each account.
- **Logging**: Provides colored logs for better clarity.
- **Automation Cycle**: Runs continuously with a one-hour delay between cycles.
---

## Requirements

- Python 3.8 or higher
- Libraries:
  - `requests`
  - `pynacl`
  - `termcolor`
  - `base58`

Install the required libraries using the command:

```bash
pip install requests pynacl termcolor base58
```

---

## File Structure

- **`accounts.txt`**: Stores account details in the format `token:refresh_token:private_key`, one account per line.
- **`proxies.txt`**: Stores proxy addresses, one per line.

---

## How to Use

1. **Prepare Account File**:
   - Create a file named `accounts.txt` in the same directory as the script.
   - Add account details in the format:
     ```
     <token>:<refresh_token>:<private_key>
     ```

2. **Prepare Proxy File** (optional):
   - Create a file named `proxies.txt` in the same directory.
   - Add proxy addresses in the format:
     ```
     http://username:password@proxy_address:port
     ```

3. **Run the Script**:
   - 1. Execute the bot using:
     ```bash
     python3 bot.py 
     ```
   

4. **Monitor Logs**:
   - Logs will display activity for each account, color-coded for clarity:
     - **Green**: Success
     - **Red**: Error
     - **Yellow**: Warning
     - **Cyan**: System messages
     - **Magenta**: General info

---

## Functionality Overview

### Account Management
- Reads accounts from `accounts.txt`.
- Updates the file with refreshed tokens.

### Proxy Handling
- Reads proxies from `proxies.txt`.
- Distributes proxies across accounts.

### Daily Reward Claims
- Claims daily points using API endpoints.
- Handles expired tokens by refreshing or re-logging.

### Logging
- Uses the `termcolor` library for colored logs.

---

- Ensure that the API endpoints and account details are correct.
- Use valid proxies to avoid network issues.
- The script runs in a continuous loop. Use `Ctrl+C` to stop it.

---


## Disclaimer
This script is provided for educational purposes only and comes with no warranty. Always use a new wallet, as any loss of assets or associated risks are your own responsibility.

## Notes
- The script is designed to handle errors gracefully and retry operations when possible.
- Ensure that the required files (`accounts.txt` and optionally `proxies.txt`) are properly formatted and placed in the script's directory.ies with applicable terms of service and laws.


## Donate
If you find this useful and would like to donate to the following wallet address:
- eth : 0x254d96A7D543279BCfA63506C1935aC843573aa0
- sol : FxXqUi5ZN8dq8EqLF1f1xkBv7Y1qzagVcq6BNQjsR1A7