# Reservation Bot

This project is a Python automation bot that allows users to automatically reserve a time slot on a website. The bot uses Selenium to interact with the website, simulating user actions in a browser. The bot logs in, searches for the desired slot, reserves it, and completes checkout with optional promo code and payment information.
All sensitive information and configurable parameters are stored in a .env file

## Features
- Automatically opens a web browser and navigates to the website.
- Logs in with credentials stored in .env file.
- Searches for a specific time slot.
- Reserves the selected time slot.
- Completes the checkout process, including payment and promo code application.
- Fully configurable via environment variables (.env) for credentials, dates, and site URLs.

## How It Works
Selenium opens a real browser window, so you can watch the automation in action:
1. Login:
The bot opens the website and logs in using the credentials provided in the .env file.
2. Navigation:
It navigates the site to find the desired time slot.
3. Reservation:
Once the time slot is found, the bot selects it and proceeds to the reservation.
4. Checkout:
The bot completes the checkout process, applying a promo code if provided and handling the payment confirmation.

## Requirements
- Python **3.7+**
- Google Chrome installed on your system
- Selenium for browser automation
- pydantic-settings for configuration management

## Setup

Clone the repository, create a virtual environment, and install the dependencies.

### macOS / Linux

```bash
# Check your Python version
python3 --version

# Clone the repo
git clone git@github.com:Ines-be/padel_bot.git
cd padel_bot

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install selenium
pip install pydantic-settings

# Run the script
python main.py
