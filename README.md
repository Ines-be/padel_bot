# Reservation Bot

This project is an **automation bot built with Python and Selenium** that streamlines the process of booking sports fields through an online reservation platform.  
It automates every step — from login and time slot selection to booking confirmation and payment — achieving faster and more reliable reservations.

## 🤖 Overview
The bot allows users to automatically reserve a time slot on a website, it uses Selenium to interact with the website, simulating user actions in a browser: the bot logs in, searches for the desired slot, reserves it, and completes checkout with optional promo code and payment information.  
All sensitive information and configurable parameters are stored in a .env file

## 🚀 Features
- **Full Automation Pipeline**  
Automatically opens a web browser and navigates to the website, logs in, searches for the selected time slot, confims booking, and completes the checkout process, including payment and promo code application.

- **Dynamic Page Handling**  
Uses dynamic wait management (`WebDriverWait`) to handle aynchonous content loading.

- **Error Handling and Logging**  
Integrated retry mecanisms, detailed logging, and exception handling for improved reliability.

- **Fully Configurable via Environment Variables**  
All credentials, dates, and site URLs are managed through a `.env` file for flexible setup and deployment.

- **Performance Boost**  
  Increased successful weekly reservations from **2 to 6** and reduced average booking time from **~2 minutes to <4 seconds**.

## 🧠 How It Works
Selenium opens a browser window, so you can watch the automation in action:
1. **Login**:
The bot opens the website and logs in using the credentials provided in the .env file.
2. **Navigation**:
It navigates the site to find the desired time slot.
3. **Reservation**:
Once the time slot is found, the bot selects it and proceeds to the reservation.
4. **Checkout**:
The bot completes the checkout process, applying a promo code if provided and handling the payment confirmation.

## ⚙️ Requirements
- Python **3.7+**
- Google Chrome installed on your system
- Selenium for browser automation
- pydantic-settings for configuration management

## 🛠️ Setup and installation

Clone the repository, create a virtual environment, and install the dependencies.

### macOS / Linux

```bash
# Check your Python version
python3 --version

# Clone the repo
git clone git@github.com:Ines-be/reservation_bot.git
cd padel_bot

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install selenium
pip install pydantic-settings

# Run the script
python main.py
