from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from datetime import datetime, timedelta
import time

# variables

MAX_ATTEMPTS = 30
MONTHS = ["Jan.", "Feb.", "Mar.", "Apr.", "May.", "Jun.", "Jul.", "Aug.", "Sep.", "Oct.", "Nov.", "Dec."]
MONTH = MONTHS[MONTH_NBR - 1]

class PadelBot:
    def __init__(self, driver):
        self.driver = driver

    def find_date(self, target_day: str, target_date: int, target_month: str):
        """Return the target date button"""
        date_buttons = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button.day-btn"))
        )

        for button in date_buttons:
            try:
                day_elem = button.find_element(By.CSS_SELECTOR, "p.day")
                date_elem = button.find_element(By.CSS_SELECTOR, "p.day-number")
                month_elem = button.find_element(By.CSS_SELECTOR, "p.month")
                
                day_text = day_elem.text.strip()
                date_text = date_elem.text.strip()
                month_text = month_elem.text.strip()
                
                if (day_text == target_day and 
                    date_text == str(target_date) and 
                    month_text == target_month):
                    return button
            except:
                continue
        
        raise Exception("Can't find the date you are looking for")

    def find_slot(self, target_slot: str):
        """Return the target slot button"""
        slot_buttons = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button.slot-button-small"))
        )

        for slot in slot_buttons:
            text = slot.text.strip()
            # print("Found slot: ", repr(text))
            if target_slot == text:
                return slot
            
        raise Exception("Can't find the slot you are looking for")

    def find_resa(self):
        """Return the target reservation button"""
        resa_infos = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.card-body-session-description"))
        )
        resa_infos = self.driver.find_elements(By.CSS_SELECTOR, "div.card-body-session-description")

        for resa in resa_infos:
            info = resa.find_element(By.CSS_SELECTOR, "p.time").text
            split = [p.strip() for p in info.split("-")]
            if len(split) >= 3:
                duration = split[-1]
                if duration == DURATION:
                    button = resa.find_element(By.XPATH, "../../following-sibling::div[@class='tarif']//button")
                    return button
                
        raise Exception("Can't find the resa you are looking for")

    def connection(self):
        """Log in to the website"""
        username = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='email']"))
        )
        password = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='password']"))
        )

        username.send_keys(USERNAME)
        password.send_keys(PASSWORD)

        self.driver.find_element(By.CSS_SELECTOR, "button.email-link-btn").click()

    def input_gymlib_codes(self):
        """Input and submit Gymlib codes"""
        promo_btn = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a.addCodePromo"))
        )
        promo_btn.click()

        gymlib_btn = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.gymlib.club"))
        )
        gymlib_btn.click()

        for i in range (len(GYMLIB_CODES)):
            gym_code = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, f"input.input[placeholder='Code gymlib du joueur {i + 1}']"))
            )
            gym_code.send_keys(GYMLIB_CODES[i])

            email = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, f"input.input[placeholder='Email gymlib du joueur {i + 1}']"))
            )
            email.send_keys(EMAILS[i])

        submit_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.submit.mx-auto"))
            )
        submit_btn.click()

    def payment_info(self):
        """Input and submit payment informations"""
        first_name = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "firstname")))
        first_name.send_keys(FIRST_NAME)

        last_name = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "lastName")))
        last_name.send_keys(LAST_NAME)

        confirm_btn = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "submit")))
        confirm_btn.click()
        print("Success: personal info filled")
        
        WebDriverWait(self.driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[title='Cadre de saisie sécurisé pour le paiement']"))
        )

        card_btn = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-value="card"]'))
        )
        card_btn.click()

        card_nbr = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "number"))
        )
        card_nbr.click()
        card_nbr.send_keys(CARD_NUMBER)

        exp = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "Field-expiryInput"))
        )
        exp.send_keys(EXP_DATE)

        cvc = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "Field-cvcInput"))
        )
        cvc.send_keys(CVC)

        print("Success: credit card info filled")
        checkout = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "submit"))
        )
        checkout.click()

    def get_date(self):
        """Search and click target date"""
        attempts = 0
        while attempts < MAX_ATTEMPTS:
            try:
                date_btn = self.find_date(DAY, DATE, MONTH)
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(date_btn)
                )
                time.sleep(0.2)
                date_btn.click()
                print("Success: date found")
                return
            except Exception as e:
                print("Error: date not found: ", e)
                self.driver.refresh()
                time.sleep(0.5)
                attempts += 1

    def get_slot(self):
        """Search and click target slot"""
        attempts = 0
        while attempts < MAX_ATTEMPTS:
            try:
                slot_btn = self.find_slot(SLOT)
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(slot_btn)
                )
                slot_btn.click()
                print("Success: slot found")
                return
            except Exception as e:
                print("Error: slot not found: ", e)
                self.driver.get(RESERVATION_PAGE)
                self.get_date()
                time.sleep(0.5)
                attempts += 1

    def get_resa(self):
        """Search and click target reservation"""
        attempts = 0
        while attempts < MAX_ATTEMPTS:
            try:
                resa_btn = self.find_resa()
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(resa_btn)
                )
                resa_btn.click()
                print("Success: resa found")
                return
            except Exception as e:
                print("Error: resa not found: ", e)
                self.driver.get(RESERVATION_PAGE)
                self.get_date()
                self.get_slot()
                time.sleep(0.5)
                attempts += 1

    def co_and_resa(self):
        """Log in and make the reservation"""
        self.driver.get(LOGIN_PAGE)

        try:
            self.connection()
            print("Success: connection")
        except:
            raise Exception("connection failed")
        
        self.driver.get(RESERVATION_PAGE)
        self.get_date()
        self.get_slot()
        self.get_resa()

def start_bot():
    """Wait until 2 seconds before the slot is available to start"""
    slot_time = SLOT.split(":")
    target_time = datetime(YEAR, MONTH_NBR, int(DATE), int(slot_time[0]), int(slot_time[1]), 0)
    print("Target slot = ", target_time, DURATION)

    start_time = target_time - timedelta(days=6, seconds=2)
    print("Start time = ", start_time)

    print("Waiting...")
    while datetime.now() < start_time:
        time.sleep(0.5)
    print("Starting")

def main():
    start_bot()

    driver = webdriver.Chrome()
    driver.get(LOGIN_PAGE)

    pb = PadelBot(driver)

    while True:
        try:
            pb.co_and_resa()
            print("Success: reservation selected")
            print("Looking for checkout page...")
            WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h3.recap-title"))
            )
            print("Website redirecting us to checkout")
            break
        except Exception as e:
            if isinstance(e, TimeoutException):
                print("Website redirected us to login...")
            else:
                print("Error: ", e)

    try:
        pb.input_gymlib_codes()

        accept = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='checkbox']"))
        )
        accept.click()
        print("Terms accepted")

        pay = driver.find_element(By.CSS_SELECTOR, "button.rcorners.btn-marginTop")
        pay.click()
        print("Pay btn clicked")

        # pb.payment_info()

    except Exception as e:
        print("Error: ", e)

    input("PRESS ENTER TO CLOSE WINDOW AND QUIT")
    driver.quit()

if __name__ == "__main__":
    main()